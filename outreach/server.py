#!/usr/bin/env python3
"""
MD DIGITAL — Vienna Lead Outreach Dashboard & Automation Server
Lightweight local web application running on standard Python libraries.
"""

import http.server
import socketserver
import urllib.parse
import json
import os
import sys

# Ensure local imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lead_manager import init_db, get_all_leads, get_lead_by_id, add_lead, update_lead_status, export_to_csv, import_from_csv
from message_engine import generate_pitch, MY_DISPLAY_PHONE

PORT = 5050

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="de" class="bg-[#f5f5f7] text-[#1d1d1f] antialiased">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MD DIGITAL · Vienna Lead Engine & Outreach Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body { font-family: 'Inter', -apple-system, sans-serif; }
        .font-mono { font-family: 'JetBrains Mono', monospace; }
        .apple-card { background: #ffffff; border: 1px solid rgba(0,0,0,0.06); box-shadow: 0 4px 20px -2px rgba(0,0,0,0.04); }
    </style>
</head>
<body class="min-h-screen p-6 max-w-7xl mx-auto space-y-8">

    <!-- Header Navigation -->
    <header class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-black/[0.08]">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-2xl bg-[#1d1d1f] text-white flex items-center justify-center font-bold text-sm shadow-sm">
                MD
            </div>
            <div>
                <h1 class="text-xl font-extrabold tracking-tight text-[#1d1d1f] flex items-center gap-2">
                    Vienna Lead & Outreach Engine
                    <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                </h1>
                <p class="text-xs text-[#86868b] font-mono">B2B Kunden-Akquise Wien · Daoud Sahel &amp; Marcel Pasik</p>
            </div>
        </div>

        <div class="flex items-center gap-3">
            <button onclick="document.getElementById('add-modal').classList.remove('hidden')" class="px-4 py-2 rounded-xl bg-[#0071e3] hover:bg-[#0077ed] text-white text-xs font-bold transition-all flex items-center gap-1.5 shadow-sm">
                <i data-lucide="plus" class="w-4 h-4"></i> Neuer Wiener Lead
            </button>
            <a href="/api/export" class="px-4 py-2 rounded-xl bg-white border border-black/[0.08] hover:bg-slate-50 text-xs font-mono font-semibold text-[#1d1d1f] transition-all flex items-center gap-1.5 shadow-sm">
                <i data-lucide="download" class="w-3.5 h-3.5"></i> CSV Export
            </a>
            <a href="https://d10ud.github.io/md-digital-websites/" target="_blank" class="px-4 py-2 rounded-xl bg-[#1d1d1f] hover:bg-black text-white text-xs font-mono font-semibold transition-all flex items-center gap-1.5">
                <i data-lucide="external-link" class="w-3.5 h-3.5"></i> Live Website
            </a>
        </div>
    </header>

    <!-- Top Stats Bento -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="apple-card p-5 rounded-2xl">
            <div class="text-[11px] font-mono text-[#86868b] uppercase">Gesamt Leads Wien</div>
            <div class="text-3xl font-extrabold font-mono text-[#1d1d1f] mt-1" id="stat-total">0</div>
            <div class="text-[11px] text-[#86868b] mt-0.5">Innere Stadt, Neubau &amp; Bezirke</div>
        </div>
        <div class="apple-card p-5 rounded-2xl">
            <div class="text-[11px] font-mono text-amber-600 uppercase font-semibold">Keine Website (Top Chance)</div>
            <div class="text-3xl font-extrabold font-mono text-amber-600 mt-1" id="stat-noweb">0</div>
            <div class="text-[11px] text-[#86868b] mt-0.5">Dringender Bedarf an 399 € Paket</div>
        </div>
        <div class="apple-card p-5 rounded-2xl">
            <div class="text-[11px] font-mono text-[#0071e3] uppercase font-semibold">Kontaktiert</div>
            <div class="text-3xl font-extrabold font-mono text-[#0071e3] mt-1" id="stat-contacted">0</div>
            <div class="text-[11px] text-[#86868b] mt-0.5">Per WhatsApp oder E-Mail</div>
        </div>
        <div class="apple-card p-5 rounded-2xl">
            <div class="text-[11px] font-mono text-emerald-600 uppercase font-semibold">Gewonnene Kunden</div>
            <div class="text-3xl font-extrabold font-mono text-emerald-600 mt-1" id="stat-won">0</div>
            <div class="text-[11px] text-[#86868b] mt-0.5">Website &amp; 4K Foto Aufträge</div>
        </div>
    </div>

    <!-- Filter Bar -->
    <div class="apple-card p-4 rounded-2xl flex flex-wrap items-center justify-between gap-4">
        <div class="flex flex-wrap items-center gap-2">
            <span class="text-xs font-mono font-semibold text-[#86868b] mr-1">Filter:</span>
            <button onclick="setFilter('all')" id="btn-filter-all" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-[#1d1d1f] text-white">Alle</button>
            <button onclick="setFilter('barber')" id="btn-filter-barber" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 text-[#1d1d1f] hover:bg-slate-200">✂️ Barber & Salons</button>
            <button onclick="setFilter('tech')" id="btn-filter-tech" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 text-[#1d1d1f] hover:bg-slate-200">📱 Tech & Repair</button>
            <button onclick="setFilter('gastro')" id="btn-filter-gastro" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 text-[#1d1d1f] hover:bg-slate-200">☕ Gastro & Cafés</button>
            <button onclick="setFilter('craft')" id="btn-filter-craft" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 text-[#1d1d1f] hover:bg-slate-200">🔨 Handwerk</button>
        </div>

        <div class="flex items-center gap-2">
            <input type="text" id="search-input" onkeyup="renderTable()" placeholder="Laden oder Bezirk suchen..." class="px-3.5 py-1.5 rounded-xl border border-black/[0.1] text-xs font-mono focus:outline-none focus:border-[#0071e3] w-56">
        </div>
    </div>

    <!-- Leads Table -->
    <div class="apple-card rounded-2xl overflow-hidden">
        <div class="overflow-x-auto">
            <table class="w-full text-left text-xs">
                <thead class="bg-[#fafafa] border-b border-black/[0.06] text-[#86868b] font-mono uppercase text-[11px]">
                    <tr>
                        <th class="py-3.5 px-4">Betrieb &amp; Bezirk</th>
                        <th class="py-3.5 px-4">Branche</th>
                        <th class="py-3.5 px-4">Website Status</th>
                        <th class="py-3.5 px-4">Kontakt</th>
                        <th class="py-3.5 px-4">Status</th>
                        <th class="py-3.5 px-4 text-right">1-Click Outreach</th>
                    </tr>
                </thead>
                <tbody id="leads-tbody" class="divide-y divide-black/[0.04]">
                    <!-- Dynamically populated -->
                </tbody>
            </table>
        </div>
    </div>

    <!-- Pitch Modal (WhatsApp & Email Preview) -->
    <div id="pitch-modal" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
        <div class="apple-card rounded-3xl max-w-2xl w-full p-6 space-y-5 bg-white shadow-2xl relative">
            <div class="flex items-center justify-between border-b border-black/[0.08] pb-4">
                <div>
                    <span class="text-[10px] font-mono uppercase tracking-widest text-[#0071e3] font-bold" id="modal-branch">BRANCHE</span>
                    <h3 class="text-xl font-bold text-[#1d1d1f]" id="modal-title">Laden Name</h3>
                </div>
                <button onclick="document.getElementById('pitch-modal').classList.add('hidden')" class="w-8 h-8 rounded-full bg-slate-100 hover:bg-slate-200 flex items-center justify-center text-[#86868b]">
                    <i data-lucide="x" class="w-4 h-4"></i>
                </button>
            </div>

            <!-- Pitch Tabs -->
            <div class="flex gap-2 border-b border-black/[0.06] pb-2">
                <button onclick="switchModalTab('wa')" id="modal-tab-wa" class="px-4 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 text-white flex items-center gap-1.5">
                    <i data-lucide="message-circle" class="w-3.5 h-3.5"></i> WhatsApp Pitch
                </button>
                <button onclick="switchModalTab('email')" id="modal-tab-email" class="px-4 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 text-[#1d1d1f] hover:bg-slate-200 flex items-center gap-1.5">
                    <i data-lucide="mail" class="w-3.5 h-3.5"></i> E-Mail Pitch
                </button>
            </div>

            <!-- WhatsApp Preview Box -->
            <div id="modal-wa-box" class="space-y-3">
                <div class="p-4 rounded-2xl bg-[#e8f5e9] border border-emerald-200 font-mono text-xs whitespace-pre-line leading-relaxed text-[#1b5e20]" id="modal-wa-text"></div>
                <div class="flex items-center justify-between gap-3 pt-2">
                    <button onclick="copyToClipboard('modal-wa-text')" class="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-xs font-semibold font-mono flex items-center gap-1.5">
                        <i data-lucide="copy" class="w-3.5 h-3.5"></i> Text kopieren
                    </button>
                    <a id="modal-wa-btn" href="#" target="_blank" class="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs flex items-center gap-2 shadow-md">
                        <i data-lucide="message-circle" class="w-4 h-4"></i> In WhatsApp öffnen
                    </a>
                </div>
            </div>

            <!-- Email Preview Box -->
            <div id="modal-email-box" class="space-y-3 hidden">
                <div class="text-xs font-mono text-[#86868b]"><strong>Betreff:</strong> <span id="modal-email-sub" class="text-[#1d1d1f]"></span></div>
                <div class="p-4 rounded-2xl bg-slate-50 border border-black/[0.08] font-mono text-xs whitespace-pre-line leading-relaxed text-[#1d1d1f] max-h-64 overflow-y-auto" id="modal-email-text"></div>
                <div class="flex items-center justify-between gap-3 pt-2">
                    <button onclick="copyToClipboard('modal-email-text')" class="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-xs font-semibold font-mono flex items-center gap-1.5">
                        <i data-lucide="copy" class="w-3.5 h-3.5"></i> Text kopieren
                    </button>
                    <a id="modal-email-btn" href="#" class="px-6 py-2.5 rounded-xl bg-[#0071e3] hover:bg-[#0077ed] text-white font-bold text-xs flex items-center gap-2 shadow-md">
                        <i data-lucide="mail" class="w-4 h-4"></i> Im Mail-Programm öffnen
                    </a>
                </div>
            </div>
        </div>
    </div>

    <!-- Add Lead Modal -->
    <div id="add-modal" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
        <div class="apple-card rounded-3xl max-w-lg w-full p-6 space-y-4 bg-white shadow-2xl relative">
            <div class="flex items-center justify-between border-b border-black/[0.08] pb-3">
                <h3 class="text-lg font-bold text-[#1d1d1f]">Neuen Betrieb aus Wien hinzufügen</h3>
                <button onclick="document.getElementById('add-modal').classList.add('hidden')" class="w-8 h-8 rounded-full bg-slate-100 hover:bg-slate-200 flex items-center justify-center text-[#86868b]">
                    <i data-lucide="x" class="w-4 h-4"></i>
                </button>
            </div>
            
            <form onsubmit="submitNewLead(event)" class="space-y-3 text-xs">
                <div>
                    <label class="block font-mono text-[#86868b] mb-1">Name des Betriebs *</label>
                    <input type="text" id="add-name" required placeholder="z. B. Fade Club 1010" class="w-full px-3.5 py-2 rounded-xl border border-black/[0.1] focus:outline-none focus:border-[#0071e3]">
                </div>
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block font-mono text-[#86868b] mb-1">Branche *</label>
                        <select id="add-branch" class="w-full px-3.5 py-2 rounded-xl border border-black/[0.1] focus:outline-none focus:border-[#0071e3] bg-white">
                            <option value="barber">Barber &amp; Friseur</option>
                            <option value="tech">Tech &amp; Reparatur</option>
                            <option value="gastro">Gastro &amp; Café</option>
                            <option value="craft">Handwerk &amp; Meister</option>
                            <option value="general">Sonstige Betriebe</option>
                        </select>
                    </div>
                    <div>
                        <label class="block font-mono text-[#86868b] mb-1">Bezirk (z. B. 1010 Wien)</label>
                        <input type="text" id="add-district" placeholder="1010 Wien" class="w-full px-3.5 py-2 rounded-xl border border-black/[0.1] focus:outline-none focus:border-[#0071e3]">
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block font-mono text-[#86868b] mb-1">Telefon / WhatsApp</label>
                        <input type="text" id="add-phone" placeholder="+43 676 ..." class="w-full px-3.5 py-2 rounded-xl border border-black/[0.1] focus:outline-none focus:border-[#0071e3]">
                    </div>
                    <div>
                        <label class="block font-mono text-[#86868b] mb-1">E-Mail</label>
                        <input type="email" id="add-email" placeholder="office@..." class="w-full px-3.5 py-2 rounded-xl border border-black/[0.1] focus:outline-none focus:border-[#0071e3]">
                    </div>
                </div>
                <div>
                    <label class="block font-mono text-[#86868b] mb-1">Bestehende Website (falls vorhanden)</label>
                    <input type="text" id="add-website" placeholder="leer lassen wenn keine Website" class="w-full px-3.5 py-2 rounded-xl border border-black/[0.1] focus:outline-none focus:border-[#0071e3]">
                </div>
                <div>
                    <label class="block font-mono text-[#86868b] mb-1">Notizen / Beobachtungen</label>
                    <input type="text" id="add-notes" placeholder="z. B. Auf Google Maps gefunden, schlechte Fotos" class="w-full px-3.5 py-2 rounded-xl border border-black/[0.1] focus:outline-none focus:border-[#0071e3]">
                </div>

                <div class="pt-2 flex justify-end gap-2">
                    <button type="button" onclick="document.getElementById('add-modal').classList.add('hidden')" class="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 font-semibold">Abbrechen</button>
                    <button type="submit" class="px-5 py-2 rounded-xl bg-[#0071e3] hover:bg-[#0077ed] text-white font-bold">Speichern &amp; Pitch generieren</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Engine Logic -->
    <script>
        let allLeads = [];
        let currentFilter = 'all';

        async function fetchLeads() {
            const res = await fetch('/api/leads');
            allLeads = await res.json();
            updateStats();
            renderTable();
        }

        function updateStats() {
            document.getElementById('stat-total').innerText = allLeads.length;
            document.getElementById('stat-noweb').innerText = allLeads.filter(l => l.has_website === 0).length;
            document.getElementById('stat-contacted').innerText = allLeads.filter(l => l.status === 'kontaktiert').length;
            document.getElementById('stat-won').innerText = allLeads.filter(l => l.status === 'gewonnen').length;
        }

        function setFilter(branch) {
            currentFilter = branch;
            ['all', 'barber', 'tech', 'gastro', 'craft'].forEach(b => {
                const btn = document.getElementById('btn-filter-' + b);
                if (b === branch) {
                    btn.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-[#1d1d1f] text-white';
                } else {
                    btn.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 text-[#1d1d1f] hover:bg-slate-200';
                }
            });
            renderTable();
        }

        function renderTable() {
            const tbody = document.getElementById('leads-tbody');
            const search = document.getElementById('search-input').value.toLowerCase();
            
            const filtered = allLeads.filter(l => {
                const matchesBranch = (currentFilter === 'all') || (l.branch === currentFilter);
                const matchesSearch = l.name.toLowerCase().includes(search) || (l.district && l.district.toLowerCase().includes(search));
                return matchesBranch && matchesSearch;
            });

            tbody.innerHTML = '';
            if (filtered.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="p-6 text-center text-[#86868b] font-mono">Keine Leads für diese Auswahl gefunden.</td></tr>';
                return;
            }

            filtered.forEach(lead => {
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-50/70 transition-colors';

                const branchIcons = {
                    barber: '✂️ Barber',
                    tech: '📱 Tech',
                    gastro: '☕ Gastro',
                    craft: '🔨 Handwerk',
                    general: '🏢 Allgemein'
                };

                const webBadge = lead.has_website === 0 
                    ? '<span class="px-2.5 py-1 rounded-full bg-amber-50 text-amber-700 border border-amber-200 font-mono font-bold text-[10px]">❌ Keine Website (Chance!)</span>'
                    : '<span class="px-2.5 py-1 rounded-full bg-slate-100 text-slate-600 font-mono text-[10px]">⚠️ Veraltete Website</span>';

                tr.innerHTML = `
                    <td class="py-3.5 px-4">
                        <div class="font-bold text-[#1d1d1f] text-sm">${lead.name}</div>
                        <div class="text-[11px] text-[#86868b] font-mono flex items-center gap-1 mt-0.5">
                            <i data-lucide="map-pin" class="w-3 h-3 text-[#0071e3]"></i> ${lead.district || 'Wien'} · ${lead.address || ''}
                        </div>
                    </td>
                    <td class="py-3.5 px-4 font-mono text-xs">
                        <span class="px-2.5 py-1 rounded-lg bg-slate-100 text-[#1d1d1f] font-semibold">${branchIcons[lead.branch] || lead.branch}</span>
                    </td>
                    <td class="py-3.5 px-4">
                        ${webBadge}
                    </td>
                    <td class="py-3.5 px-4 font-mono text-xs space-y-0.5">
                        ${lead.phone ? `<div><a href="tel:${lead.phone}" class="hover:text-[#0071e3] flex items-center gap-1"><i data-lucide="phone" class="w-3 h-3 text-slate-400"></i> ${lead.phone}</a></div>` : '<span class="text-slate-300">Keine Nr.</span>'}
                        ${lead.email ? `<div><a href="mailto:${lead.email}" class="hover:text-[#0071e3] text-slate-500 flex items-center gap-1"><i data-lucide="mail" class="w-3 h-3 text-slate-400"></i> ${lead.email}</a></div>` : ''}
                    </td>
                    <td class="py-3.5 px-4">
                        <select onchange="updateStatus(${lead.id}, this.value)" class="px-2 py-1 rounded-lg border border-black/[0.1] font-mono text-[11px] bg-white font-semibold">
                            <option value="neu" ${lead.status === 'neu' ? 'selected' : ''}>🔵 Neu</option>
                            <option value="kontaktiert" ${lead.status === 'kontaktiert' ? 'selected' : ''}>🟡 Kontaktiert</option>
                            <option value="geantwortet" ${lead.status === 'geantwortet' ? 'selected' : ''}>🟣 Geantwortet</option>
                            <option value="termin" ${lead.status === 'termin' ? 'selected' : ''}>🟠 Termin vereinbart</option>
                            <option value="gewonnen" ${lead.status === 'gewonnen' ? 'selected' : ''}>🟢 Deal gewonnen</option>
                        </select>
                    </td>
                    <td class="py-3.5 px-4 text-right">
                        <div class="flex items-center justify-end gap-1.5">
                            <button onclick="openPitch(${lead.id})" class="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 font-mono font-semibold flex items-center gap-1" title="Pitch ansehen & anpassen">
                                <i data-lucide="eye" class="w-3.5 h-3.5"></i> Vorschau
                            </button>
                            ${lead.phone ? `
                            <a href="#" onclick="launchWhatsApp(${lead.id}); return false;" class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-mono font-bold flex items-center gap-1 shadow-sm" title="Direkt per WhatsApp kontaktieren">
                                <i data-lucide="message-circle" class="w-3.5 h-3.5"></i> WhatsApp
                            </a>` : ''}
                        </div>
                    </td>
                `;
                tbody.appendChild(tr);
            });
            lucide.createIcons();
        }

        async function updateStatus(id, newStatus) {
            await fetch('/api/status', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({id: id, status: newStatus})
            });
            const lead = allLeads.find(l => l.id === id);
            if (lead) lead.status = newStatus;
            updateStats();
        }

        async function openPitch(id) {
            const res = await fetch('/api/pitch?id=' + id);
            const pitch = await res.json();

            document.getElementById('modal-title').innerText = pitch.name;
            document.getElementById('modal-branch').innerText = pitch.branch.toUpperCase() + ' · ' + pitch.district;

            document.getElementById('modal-wa-text').innerText = pitch.whatsapp_body;
            document.getElementById('modal-wa-btn').href = pitch.whatsapp_url;

            document.getElementById('modal-email-sub').innerText = pitch.subject;
            document.getElementById('modal-email-text').innerText = pitch.email_body;
            document.getElementById('modal-email-btn').href = pitch.mailto_url;

            switchModalTab('wa');
            document.getElementById('pitch-modal').classList.remove('hidden');
            lucide.createIcons();
        }

        function switchModalTab(tab) {
            if (tab === 'wa') {
                document.getElementById('modal-wa-box').classList.remove('hidden');
                document.getElementById('modal-email-box').classList.add('hidden');
                document.getElementById('modal-tab-wa').className = 'px-4 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 text-white flex items-center gap-1.5';
                document.getElementById('modal-tab-email').className = 'px-4 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 text-[#1d1d1f] hover:bg-slate-200 flex items-center gap-1.5';
            } else {
                document.getElementById('modal-wa-box').classList.add('hidden');
                document.getElementById('modal-email-box').classList.remove('hidden');
                document.getElementById('modal-tab-wa').className = 'px-4 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 text-[#1d1d1f] hover:bg-slate-200 flex items-center gap-1.5';
                document.getElementById('modal-tab-email').className = 'px-4 py-1.5 rounded-lg text-xs font-semibold bg-[#0071e3] text-white flex items-center gap-1.5';
            }
        }

        async function launchWhatsApp(id) {
            const res = await fetch('/api/pitch?id=' + id);
            const pitch = await res.json();
            if (pitch.whatsapp_url) {
                updateStatus(id, 'kontaktiert');
                window.open(pitch.whatsapp_url, '_blank');
            } else {
                alert('Für diesen Betrieb ist keine Mobilfunknummer hinterlegt.');
            }
        }

        async function submitNewLead(e) {
            e.preventDefault();
            const data = {
                name: document.getElementById('add-name').value,
                branch: document.getElementById('add-branch').value,
                district: document.getElementById('add-district').value,
                phone: document.getElementById('add-phone').value,
                email: document.getElementById('add-email').value,
                website: document.getElementById('add-website').value,
                notes: document.getElementById('add-notes').value
            };
            await fetch('/api/add', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            document.getElementById('add-modal').classList.add('hidden');
            document.getElementById('add-name').value = '';
            fetchLeads();
        }

        function copyToClipboard(elementId) {
            const text = document.getElementById(elementId).innerText;
            navigator.clipboard.writeText(text);
            alert('Text in die Zwischenablage kopiert!');
        }

        // Init
        fetchLeads();
    </script>
</body>
</html>
"""

class OutreachHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/" or path == "/dashboard":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))

        elif path == "/api/leads":
            leads = get_all_leads()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(leads).encode("utf-8"))

        elif path == "/api/pitch":
            lead_id = query.get("id", [None])[0]
            if lead_id:
                lead = get_lead_by_id(int(lead_id))
                if lead:
                    pitch = generate_pitch(lead)
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(json.dumps(pitch).encode("utf-8"))
                    return
            self.send_response(404)
            self.end_headers()

        elif path == "/api/export":
            export_file = os.path.join(os.path.dirname(__file__), "vienna_leads_export.csv")
            export_to_csv(export_file)
            with open(export_file, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/csv")
            self.send_header("Content-Disposition", "attachment; filename=vienna_leads_export.csv")
            self.end_headers()
            self.wfile.write(content)

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        data = json.loads(body) if body else {}

        if path == "/api/status":
            lead_id = data.get("id")
            new_status = data.get("status")
            if lead_id and new_status:
                update_lead_status(lead_id, new_status)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
                return

        elif path == "/api/add":
            lead_id = add_lead(
                name=data.get("name", ""),
                branch=data.get("branch", "general"),
                district=data.get("district", ""),
                address="",
                phone=data.get("phone", ""),
                email=data.get("email", ""),
                website=data.get("website", ""),
                has_website=1 if data.get("website") else 0,
                notes=data.get("notes", "")
            )
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "lead_id": lead_id}).encode("utf-8"))
            return

        self.send_response(400)
        self.end_headers()

    def log_message(self, format, *args):
        # Silence routine request logging
        return

def run_server():
    init_db()
    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), OutreachHandler) as httpd:
        print(f"🚀 MD DIGITAL Outreach Dashboard läuft auf http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer beendet.")

if __name__ == "__main__":
    run_server()

import os
import re
import time

import google.generativeai as genai
import gradio as gr


def extract_html_code(text: str):
    # Extract the HTML code from the response
    match = re.search(r"```html(.*)```", text, re.DOTALL)
    if match:
        return match.group(1)
    else:
        raise ValueError("No HTML code block found in the text")


api_key = os.getenv("GOOGLE_API_KEY", "")

supported_models = [
    "models/gemini-2.5-flash-preview-04-17",
    "gemini-2.5-pro-preview-05-06",
]

few_shot_examples = """
EXAMPLE BEGINNING

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vols</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
    <style>
        body {
            font-family: 'Google Sans', sans-serif; /* Fallback to sans-serif if Google Sans not available */
        }
        /* Custom scrollbar for webkit browsers */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #2d3748; /* gray-800 */
        }
        ::-webkit-scrollbar-thumb {
            background: #4a5568; /* gray-600 */
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #718096; /* gray-500 */
        }
        .active-nav {
            border-bottom: 2px solid #4285F4;
            color: #4285F4;
        }
        .date-input-active {
            border-color: #4285F4 !important;
        }
        .calendar-day.selected-start, .calendar-day.selected-end {
            background-color: #4285F4;
            color: white;
            border-radius: 50%;
        }
        .calendar-day.in-range {
            background-color: #D1E3FF; /* Lighter blue */
            color: #1A73E8; /* Darker blue text */
            border-radius: 0;
        }
        .calendar-day.selected-start.in-range { /* Adjust start if it's part of a range */
             border-top-right-radius: 0;
             border-bottom-right-radius: 0;
        }
        .calendar-day.selected-end.in-range { /* Adjust end if it's part of a range */
            border-top-left-radius: 0;
            border-bottom-left-radius: 0;
        }
        .calendar-day:not(.disabled-day):hover {
            outline: 1px solid #A0A0A0;
            border-radius: 50%;
        }
        .calendar-day.disabled-day {
            color: #718096; /* gray-500 */
            pointer-events: none;
        }
        .placeholder-bg { /* TODO: Add image asset: Stylized mountain landscape background */
            background-image: url("data:image/svg+xml,%3Csvg width='800' height='200' viewBox='0 0 800 200' xmlns='http://www.w3.org/2000/svg'%3E%3Crect width='800' height='200' fill='%231a202c'/%3E%3Ctext x='50%25' y='50%25' font-family='Arial' font-size='20' fill='%23a0aec0' dominant-baseline='middle' text-anchor='middle'%3EBackground Image Placeholder%3C/text%3E%3C/svg%3E");
            background-size: cover;
            background-position: center;
            opacity: 0.6;
        }
    </style>
</head>
<body class="bg-gray-900 text-gray-200">
    <header class="p-4 flex justify-between items-center">
        <div class="flex items-center space-x-8">
            <!-- TODO: Add SVG asset: Voyager logo -->
            <span class="text-xl font-bold">Voyager</span>
            <nav class="flex space-x-6 text-sm">
                <a href="#" class="hover:text-blue-400 flex items-center space-x-1">
                    <i class="fas fa-search"></i> <!-- Placeholder for Explorer icon -->
                    <span>Explorer</span>
                </a>
                <a href="#" class="active-nav font-semibold flex items-center space-x-1">
                    <i class="fas fa-plane"></i> <!-- Placeholder for Vols icon -->
                    <span>Vols</span>
                </a>
                <a href="#" class="hover:text-blue-400 flex items-center space-x-1">
                    <i class="fas fa-bed"></i> <!-- Placeholder for Hôtels icon -->
                    <span>Hôtels</span>
                </a>
                <a href="#" class="hover:text-blue-400 flex items-center space-x-1">
                    <i class="fas fa-home"></i> <!-- Placeholder for Locations de vacances icon -->
                    <span>Locations de vacances</span>
                </a>
            </nav>
        </div>
        <!-- TODO: Add SVG asset: User profile icon -->
        <div class="w-8 h-8 bg-gray-700 rounded-full flex items-center justify-center">
            <i class="fas fa-user"></i>
        </div>
    </header>

    <main class="relative">
        <div class="absolute inset-0 placeholder-bg z-0"></div>
        <div class="relative z-10 pt-16 pb-8 px-4 md:px-20 flex flex-col items-center">
            <h1 class="text-5xl font-bold mb-8 text-white">Vols</h1>

            <div class="bg-gray-800 p-4 rounded-lg shadow-xl w-full max-w-3xl">
                <div class="flex flex-col sm:flex-row sm:items-center space-y-2 sm:space-y-0 sm:space-x-2 mb-3">
                    <button class="bg-gray-700 hover:bg-gray-600 text-sm px-3 py-2 rounded-md flex items-center justify-center sm:justify-start">
                        <i class="fas fa-exchange-alt mr-2"></i> Aller-retour <i class="fas fa-caret-down ml-auto sm:ml-2"></i>
                    </button>
                    <button class="bg-gray-700 hover:bg-gray-600 text-sm px-3 py-2 rounded-md flex items-center justify-center sm:justify-start">
                        <i class="fas fa-user mr-2"></i> 1 <i class="fas fa-caret-down ml-auto sm:ml-2"></i>
                    </button>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-1 gap-0 mb-3">
                     <div class="bg-gray-700 p-3 rounded-md flex items-center">
                        <!-- TODO: Add SVG asset: Radio button like circle for origin input -->
                        <i class="far fa-circle mr-3 text-blue-400"></i>
                        <input type="text" placeholder="Paris" class="bg-transparent w-full focus:outline-none text-white placeholder-gray-400">
                    </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-px bg-gray-600 rounded-md overflow-hidden">
                    <div id="departInputDisplay" class="date-input bg-gray-700 p-3 flex items-center cursor-pointer border-2 border-gray-700 hover:border-gray-500">
                        <!-- TODO: Add SVG asset: Calendar icon -->
                        <i class="fas fa-calendar-alt mr-3 text-gray-400"></i>
                        <span class="text-gray-100">Départ</span>
                    </div>
                    <div id="retourInputDisplay" class="date-input bg-gray-700 p-3 flex items-center cursor-pointer border-2 border-gray-700 hover:border-gray-500">
                         <!-- TODO: Add SVG asset: Calendar icon (same as above) -->
                        <i class="fas fa-calendar-alt mr-3 text-gray-400"></i>
                        <span class="text-gray-100">Retour</span>
                    </div>
                </div>

                <!-- Date Picker Panel -->
                <div id="datePickerPanel" class="hidden mt-2 bg-gray-800 rounded-md shadow-lg">
                    <div class="flex justify-between items-center p-3 border-b border-gray-700">
                        <div class="text-sm text-gray-300 px-3 py-1 rounded-md bg-gray-700 hover:bg-gray-600 cursor-pointer">
                            Aller-retour <i class="fas fa-caret-down ml-1"></i>
                        </div>
                        <button id="resetDatesButton" class="hidden text-sm text-blue-400 hover:text-blue-300 px-3 py-1">Réinitialiser</button>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 p-3">
                        <div id="month1Container">
                            <h3 class="text-center font-semibold text-sm mb-2" id="month1Name">mai</h3>
                            <div class="grid grid-cols-7 gap-1 text-xs text-center text-gray-400 mb-1">
                                <span>L</span><span>M</span><span>M</span><span>J</span><span>V</span><span>S</span><span>D</span>
                            </div>
                            <div class="grid grid-cols-7 gap-1 text-sm text-center" id="month1Days">
                                <!-- Days will be populated by JS -->
                            </div>
                        </div>
                        <div id="month2Container">
                            <h3 class="text-center font-semibold text-sm mb-2" id="month2Name">juin</h3>
                            <div class="grid grid-cols-7 gap-1 text-xs text-center text-gray-400 mb-1">
                                <span>L</span><span>M</span><span>M</span><span>J</span><span>V</span><span>S</span><span>D</span>
                            </div>
                            <div class="grid grid-cols-7 gap-1 text-sm text-center" id="month2Days">
                                <!-- Days will be populated by JS -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <section class="py-8 px-4 md:px-20 bg-gray-850">
        <h2 class="text-xl font-semibold mb-4 text-gray-100">Trouvez des vols à petit prix vers ces destinations</h2>
        <div class="flex space-x-3">
            <button class="bg-gray-700 hover:bg-gray-600 text-gray-200 px-4 py-2 rounded-full text-sm">Paris</button>
            <button class="bg-gray-700 hover:bg-gray-600 text-gray-200 px-4 py-2 rounded-full text-sm">Bruxelles</button>
            <button class="bg-gray-700 hover:bg-gray-600 text-gray-200 px-4 py-2 rounded-full text-sm">Lille</button>
        </div>
    </section>

    <script>
        const departInputDisplay = document.getElementById('departInputDisplay');
        const retourInputDisplay = document.getElementById('retourInputDisplay');
        const datePickerPanel = document.getElementById('datePickerPanel');
        const resetDatesButton = document.getElementById('resetDatesButton');

        const month1NameEl = document.getElementById('month1Name');
        const month1DaysEl = document.getElementById('month1Days');
        const month2NameEl = document.getElementById('month2Name');
        const month2DaysEl = document.getElementById('month2Days');

        let selectedDepartureDate = null;
        let selectedReturnDate = null;
        let currentPickingFor = 'depart'; // 'depart', 'retour'

        // For this example, let's use fixed months like in the video: May and June 2024
        // Note: JavaScript months are 0-indexed (0=Jan, 4=May, 5=June)
        const year = 2024;
        const month1 = 4; // May
        const month2 = 5; // June
        const monthNames = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"];

        function getDaysInMonth(year, month) {
            return new Date(year, month + 1, 0).getDate();
        }

        function getFirstDayOfMonth(year, month) {
            let day = new Date(year, month, 1).getDay();
            return day === 0 ? 6 : day - 1; // Adjust so Monday is 0, Sunday is 6
        }

        function renderCalendar(year, month, monthNameEl, daysEl) {
            monthNameEl.textContent = monthNames[month];
            daysEl.innerHTML = '';

            const daysInMonth = getDaysInMonth(year, month);
            const firstDay = getFirstDayOfMonth(year, month);

            for (let i = 0; i < firstDay; i++) {
                const emptyCell = document.createElement('div');
                daysEl.appendChild(emptyCell);
            }

            for (let day = 1; day <= daysInMonth; day++) {
                const dayCell = document.createElement('div');
                dayCell.textContent = day;
                dayCell.classList.add('calendar-day', 'p-1', 'cursor-pointer', 'h-8', 'w-8', 'flex', 'items-center', 'justify-center');
                const date = new Date(year, month, day);

                // Disable past dates (simple version: all dates before today)
                // const today = new Date();
                // today.setHours(0,0,0,0);
                // if (date < today) {
                //    dayCell.classList.add('disabled-day');
                // }


                dayCell.addEventListener('click', () => handleDateClick(year, month, day));
                daysEl.appendChild(dayCell);
            }
            updateCalendarHighlights();
        }

        function handleDateClick(year, month, day) {
            const clickedDate = new Date(year, month, day);
            clickedDate.setHours(0,0,0,0); // Normalize time

            if (currentPickingFor === 'depart') {
                selectedDepartureDate = clickedDate;
                selectedReturnDate = null; // Clear return date if re-picking departure
                currentPickingFor = 'retour';
                resetDatesButton.classList.remove('hidden');
                // departInputDisplay.classList.remove('date-input-active');
                // retourInputDisplay.classList.add('date-input-active'); // Visual cue for next selection
            } else if (currentPickingFor === 'retour') {
                if (clickedDate >= selectedDepartureDate) {
                    selectedReturnDate = clickedDate;
                    // currentPickingFor = 'depart'; // Or 'done', then close picker or wait for another action
                    // retourInputDisplay.classList.remove('date-input-active');
                    // departInputDisplay.classList.add('date-input-active');
                } else { // Clicked before departure date, so treat as new departure
                    selectedDepartureDate = clickedDate;
                    selectedReturnDate = null;
                    // currentPickingFor stays 'retour'
                }
            }
            updateCalendarHighlights();
        }

        function updateCalendarHighlights() {
            document.querySelectorAll('.calendar-day').forEach(cell => {
                cell.classList.remove('selected-start', 'selected-end', 'in-range');
                if (!cell.textContent) return; // Skip empty cells

                const day = parseInt(cell.textContent);
                const cellMonthName = cell.closest('.grid.grid-cols-1.md\\:grid-cols-2 > div').querySelector('h3').textContent;
                const cellMonth = monthNames.indexOf(cellMonthName.toLowerCase());

                if (cellMonth === -1) return; // Should not happen

                const cellDate = new Date(year, cellMonth, day);
                cellDate.setHours(0,0,0,0);

                if (selectedDepartureDate && cellDate.getTime() === selectedDepartureDate.getTime()) {
                    cell.classList.add('selected-start');
                }
                if (selectedReturnDate && cellDate.getTime() === selectedReturnDate.getTime()) {
                    cell.classList.add('selected-end');
                }
                if (selectedDepartureDate && selectedReturnDate && cellDate > selectedDepartureDate && cellDate < selectedReturnDate) {
                    cell.classList.add('in-range');
                }
                // For single day range, or when start/end are part of range visually
                if (selectedDepartureDate && selectedReturnDate && selectedDepartureDate.getTime() !== selectedReturnDate.getTime()) {
                    if (cell.classList.contains('selected-start') && cellDate < selectedReturnDate) {
                        cell.classList.add('in-range'); // for styling half-backgrounds
                    }
                    if (cell.classList.contains('selected-end') && cellDate > selectedDepartureDate) {
                        cell.classList.add('in-range');
                    }
                }
            });
        }

        function toggleDatePicker() {
            const isOpen = !datePickerPanel.classList.contains('hidden');
            if (isOpen) {
                datePickerPanel.classList.add('hidden');
                departInputDisplay.classList.remove('date-input-active');
                retourInputDisplay.classList.remove('date-input-active');
            } else {
                datePickerPanel.classList.remove('hidden');
                departInputDisplay.classList.add('date-input-active'); // Default active input
                retourInputDisplay.classList.remove('date-input-active');
                currentPickingFor = 'depart'; // Reset picking context when opening
                renderCalendar(year, month1, month1NameEl, month1DaysEl);
                renderCalendar(year, month2, month2NameEl, month2DaysEl);
            }
        }

        departInputDisplay.addEventListener('click', () => {
            if (datePickerPanel.classList.contains('hidden')) {
                toggleDatePicker();
            }
            departInputDisplay.classList.add('date-input-active');
            retourInputDisplay.classList.remove('date-input-active');
            currentPickingFor = 'depart';
        });

        retourInputDisplay.addEventListener('click', () => {
            if (datePickerPanel.classList.contains('hidden')) {
                toggleDatePicker();
            }
            // Only allow focusing if departure is selected, or open picker normally.
            // For simplicity here, just open/activate.
            retourInputDisplay.classList.add('date-input-active');
            departInputDisplay.classList.remove('date-input-active');
            if (selectedDepartureDate) { // If a departure is already selected, we are picking for return
                 currentPickingFor = 'retour';
            } else { // Otherwise, treat as opening for departure first
                 currentPickingFor = 'depart';
                 departInputDisplay.classList.add('date-input-active');
                 retourInputDisplay.classList.remove('date-input-active');
            }
        });

        resetDatesButton.addEventListener('click', () => {
            selectedDepartureDate = null;
            selectedReturnDate = null;
            resetDatesButton.classList.add('hidden');
            currentPickingFor = 'depart';
            departInputDisplay.classList.add('date-input-active');
            retourInputDisplay.classList.remove('date-input-active');
            updateCalendarHighlights();
        });

        // Initial render (optional, if picker is open by default for dev)
        // renderCalendar(year, month1, month1NameEl, month1DaysEl);
        // renderCalendar(year, month2, month2NameEl, month2DaysEl);

        // Close date picker if clicking outside
        document.addEventListener('click', function(event) {
            const isClickInsideForm = departInputDisplay.contains(event.target) ||
                                      retourInputDisplay.contains(event.target) ||
                                      datePickerPanel.contains(event.target);

            if (!isClickInsideForm && !datePickerPanel.classList.contains('hidden')) {
                datePickerPanel.classList.add('hidden');
                departInputDisplay.classList.remove('date-input-active');
                retourInputDisplay.classList.remove('date-input-active');
            }
        });

    </script>
</body>
</html>
```

EXAMPLE ENDING
"""

hf_example = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hugging Face UI Clone</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #111827; /* gray-900 */
            color: #d1d5db; /* gray-300 */
        }
        .sidebar-link {
            @apply flex items-center space-x-3 px-3 py-2 text-sm font-medium rounded-md hover:bg-gray-700 hover:text-white transition-colors;
        }
        .sidebar-link.active {
            @apply bg-gray-700 text-white;
        }
        .main-content-tab {
            @apply px-3 py-1.5 text-sm font-medium rounded-md hover:bg-gray-700 cursor-pointer;
        }
        .main-content-tab.active {
            @apply bg-gray-700 text-white;
        }
        .post-card {
            @apply bg-gray-800 border border-gray-700 rounded-lg p-4 mb-4;
        }
        .trending-item-card {
            @apply bg-gray-800 border border-gray-700 rounded-lg p-3 mb-3;
        }
        /* Custom scrollbar for webkit browsers */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #1f2937; /* gray-800 */
        }
        ::-webkit-scrollbar-thumb {
            background: #4b5563; /* gray-600 */
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #6b7280; /* gray-500 */
        }
    </style>
</head>
<body class="overflow-x-hidden">
    <header class="bg-gray-800 border-b border-gray-700 sticky top-0 z-50">
        <div class="container mx-auto px-4 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-6">
                <div class="text-xl font-bold text-white">Hugging Face</div>
                <div class="relative">
                    <input type="search" placeholder="Search models, datasets, users..." class="bg-gray-700 text-gray-300 placeholder-gray-500 rounded-md py-2 px-4 pl-10 w-72 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <i class="fas fa-search text-gray-400"></i>
                    </div>
                </div>
            </div>
            <nav class="flex items-center space-x-4 text-sm font-medium">
                <a href="#" class="hover:text-white flex items-center space-x-1"><i class="fas fa-brain"></i><span>Models</span></a>
                <a href="#" class="hover:text-white flex items-center space-x-1"><i class="fas fa-database"></i><span>Datasets</span></a>
                <a href="#" class="hover:text-white flex items-center space-x-1"><i class="fas fa-rocket"></i><span>Spaces</span></a>
                <a href="#" class="text-yellow-400 hover:text-yellow-300 flex items-center space-x-1"><i class="fas fa-pen-alt"></i><span>Posts</span></a>
                <a href="#" class="hover:text-white flex items-center space-x-1"><i class="fas fa-book"></i><span>Docs</span></a>
                <a href="#" class="hover:text-white">Enterprise</a>
                <a href="#" class="hover:text-white">Pricing</a>
                <div class="w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center text-white">
                    <i class="fas fa-user"></i>
                </div>
            </nav>
        </div>
    </header>

    <div class="flex">
        <aside class="w-64 bg-gray-800 border-r border-gray-700 p-4 space-y-6 h-[calc(100vh-4rem)] sticky top-16 overflow-y-auto">
            <div>
                <button class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-md flex items-center justify-center space-x-2">
                    <i class="fas fa-plus"></i>
                    <span>New</span>
                </button>
            </div>

            <div>
                <h3 class="text-xs text-gray-500 font-semibold uppercase tracking-wider mb-2 px-3">dhuynh95</h3>
                <nav class="space-y-1">
                    <a href="#" class="sidebar-link active"><i class="fas fa-user-circle w-5 h-5"></i><span>Profile</span></a>
                    <a href="#" class="sidebar-link flex justify-between items-center">
                        <div class="flex items-center space-x-3"><i class="fas fa-inbox w-5 h-5"></i><span>Inbox</span></div>
                        <span class="bg-blue-500 text-white text-xs font-semibold px-2 py-0.5 rounded-full">143</span>
                    </a>
                    <a href="#" class="sidebar-link"><i class="fas fa-cog w-5 h-5"></i><span>Settings</span></a>
                    <a href="#" class="sidebar-link"><i class="fas fa-credit-card w-5 h-5"></i><span>Billing</span></a>
                </nav>
            </div>

            <div>
                <h3 class="text-xs text-gray-500 font-semibold uppercase tracking-wider mb-2 px-3">Organizations</h3>
                <nav class="space-y-1">
                    <a href="#" class="sidebar-link"><i class="fas fa-users w-5 h-5"></i><span>BigCode</span></a>
                    <a href="#" class="sidebar-link"><i class="fas fa-shield-alt w-5 h-5"></i><span>Mithril Security</span></a>
                    <a href="#" class="sidebar-link"><i class="fas fa-feather-alt w-5 h-5"></i><span>Blog-explorers</span></a>
                    <a href="#" class="sidebar-link"><i class="fas fa-bolt w-5 h-5"></i><span>BigAction</span></a>
                    <a href="#" class="sidebar-link"><i class="fas fa-water w-5 h-5"></i><span>LaVague</span></a>
                    <a href="#" class="sidebar-link"><i class="fas fa-comments w-5 h-5"></i><span>Social Post Explorers</span></a>
                    <a href="#" class="sidebar-link"><i class="fab fa-discord w-5 h-5"></i><span>Hugging Face Discord</span></a>
                    <a href="#" class="sidebar-link"><i class="fas fa-globe w-5 h-5"></i><span>Community</span></a>
                    <a href="#" class="sidebar-link text-blue-400 hover:text-blue-300"><i class="fas fa-plus-circle w-5 h-5"></i><span>Create New</span></a>
                </nav>
            </div>

            <div>
                <h3 class="text-xs text-gray-500 font-semibold uppercase tracking-wider mb-2 px-3">Resources</h3>
                <nav class="space-y-1">
                    <a href="#" class="sidebar-link"><i class="fas fa-compass w-5 h-5"></i><span>Hub guide</span></a>
                    <a href="#" class="sidebar-link"><i class="fas fa-file-code w-5 h-5"></i><span>Transformers doc</span></a>
                    <a href="#" class="sidebar-link"><i class="fas fa-comments w-5 h-5"></i><span>Forum</span></a>
                    <a href="#" class="sidebar-link"><i class="fas fa-tasks w-5 h-5"></i><span>Tasks</span></a>
                    <a href="#" class="sidebar-link"><i class="fas fa-graduation-cap w-5 h-5"></i><span>Learn</span></a>
                </nav>
            </div>

            <div class="pt-4 border-t border-gray-700">
                 <a href="#" class="sidebar-link"><i class="fas fa-sun w-5 h-5"></i><span>Light theme</span></a>
            </div>
        </aside>

        <main class="flex-1 p-6 bg-gray-900 h-[calc(100vh-4rem)] overflow-y-auto">
            <div class="flex items-center justify-between mb-6">
                <h1 class="text-2xl font-semibold text-white">Social Post Explorers</h1>
                <button class="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-md flex items-center space-x-2">
                    <i class="fas fa-edit"></i>
                    <span>New Post</span>
                </button>
            </div>

            <div class="flex items-center justify-between mb-4">
                <div class="flex space-x-1 bg-gray-800 p-1 rounded-lg">
                    <button class="main-content-tab active">Trending</button>
                    <button class="main-content-tab">last 7 days</button>
                </div>
            </div>

            <div class="mb-4 border-b border-gray-700">
                <nav class="flex space-x-2 -mb-px" aria-label="Tabs">
                    <a href="#" class="whitespace-nowrap py-3 px-1 border-b-2 font-medium text-sm border-blue-500 text-blue-400">All</a>
                    <a href="#" class="whitespace-nowrap py-3 px-1 border-b-2 font-medium text-sm border-transparent text-gray-400 hover:text-gray-200 hover:border-gray-500">Models</a>
                    <a href="#" class="whitespace-nowrap py-3 px-1 border-b-2 font-medium text-sm border-transparent text-gray-400 hover:text-gray-200 hover:border-gray-500">Datasets</a>
                    <a href="#" class="whitespace-nowrap py-3 px-1 border-b-2 font-medium text-sm border-transparent text-gray-400 hover:text-gray-200 hover:border-gray-500">Spaces</a>
                    <a href="#" class="whitespace-nowrap py-3 px-1 border-b-2 font-medium text-sm border-transparent text-gray-400 hover:text-gray-200 hover:border-gray-500">Papers</a>
                    <a href="#" class="whitespace-nowrap py-3 px-1 border-b-2 font-medium text-sm border-transparent text-gray-400 hover:text-gray-200 hover:border-gray-500">Collections</a>
                    <a href="#" class="whitespace-nowrap py-3 px-1 border-b-2 font-medium text-sm border-transparent text-gray-400 hover:text-gray-200 hover:border-gray-500">Community</a>
                    <a href="#" class="whitespace-nowrap py-3 px-1 border-b-2 font-medium text-sm border-transparent text-gray-400 hover:text-gray-200 hover:border-gray-500">Posts</a>
                    <a href="#" class="whitespace-nowrap py-3 px-1 border-b-2 font-medium text-sm border-transparent text-gray-400 hover:text-gray-200 hover:border-gray-500">Articles</a>
                </nav>
            </div>


            <div>
                <div class="post-card">
                    <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center space-x-2">
                            <div class="w-8 h-8 bg-indigo-500 rounded-full"></div>
                            <span class="font-semibold text-white">as-cle-bert</span>
                            <span class="text-gray-500 text-sm">posted an update</span>
                        </div>
                        <span class="text-gray-500 text-sm">5 days ago</span>
                    </div>
                    <div class="mb-3">
                        <span class="bg-yellow-500 text-yellow-900 text-xs font-semibold px-2 py-0.5 rounded-full mr-2">Post</span>
                        <span class="text-sm text-gray-400"># 1259 <i class="fas fa-fire text-orange-500"></i></span>
                    </div>
                    <p class="text-gray-300 mb-3">
                        Let's pipe some data from the web into our vector database, shall we? 🦉
                    </p>
                    <p class="text-gray-400 text-sm mb-3">
                        With <a href="#" class="text-blue-400 hover:underline">ingest-anything v1.3.0</a> ( <a href="https://github.com/AstraBert/ingest-anything" class="text-blue-400 hover:underline">https://github.com/AstraBert/ingest-anything</a> ) you can now scrape content simply starting from URLs, extract the text from it, chunk it and put it into your favorite Llamaindex-compatible database! 🥳
                    </p>
                    <p class="text-gray-400 text-sm mb-4">
                        You can do it thanks to <a href="#" class="text-blue-400 hover:underline">crawlee</a> by Apify, an open-source crawling library for python and javascript that handles all the data flow from the web: ingest-anything then combines it with BeautifulSoup, PdfItDown ar... <button class="text-blue-400 hover:underline text-xs">read more</button>
                    </p>
                    <img src="https://placehold.co/500x150/2d3748/a0aec0?text=Code+Screenshot+Placeholder" alt="Code screenshot placeholder" class="rounded-md border border-gray-700 mb-4 max-w-md">

                    <div class="flex items-center space-x-4 text-gray-500 text-sm">
                        <button class="hover:text-blue-400"><i class="fas fa-comment-alt mr-1"></i> 2 replies</button>
                        <button class="hover:text-green-400"><i class="fas fa-thumbs-up mr-1"></i> 6</button>
                        <button class="hover:text-red-400"><i class="fas fa-thumbs-down mr-1"></i></button>
                        <button class="ml-auto hover:text-gray-300">Reply</button>
                    </div>
                </div>

                <div class="post-card">
                    <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center space-x-2">
                            <div class="w-8 h-8 bg-pink-500 rounded-full"></div>
                            <span class="font-semibold text-white">JunhaoZhuang</span>
                            <span class="text-gray-500 text-sm">authored a paper</span>
                        </div>
                        <span class="text-gray-500 text-sm">9 days ago</span>
                    </div>
                     <p class="text-lg font-semibold text-white mb-1">FlexiAct: Towards Flexible Action Control in Heterogeneous Scenarios</p>
                    <div class="text-sm text-gray-500 mb-3">
                        <i class="fas fa-file-alt"></i> Paper - 2505.03730 - Published 10 days ago - <i class="fas fa-users"></i> 25
                    </div>
                     <div class="flex items-center space-x-4 text-gray-500 text-sm">
                        <button class="hover:text-blue-400"><i class="fas fa-comment-alt mr-1"></i> Reply</button>
                    </div>
                </div>

                <div class="post-card">
                    <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center space-x-2">
                             <div class="w-8 h-8 bg-teal-500 rounded-full"></div>
                            <span class="font-semibold text-white">Teemu</span>
                            <span class="text-gray-500 text-sm">posted an update</span>
                        </div>
                        <span class="text-gray-500 text-sm">11 days ago</span>
                    </div>
                     <div class="mb-3">
                        <span class="bg-yellow-500 text-yellow-900 text-xs font-semibold px-2 py-0.5 rounded-full mr-2">Post</span>
                         <span class="text-sm text-gray-400"># 915 <i class="fas fa-arrow-down text-red-500"></i></span>
                    </div>
                    <p class="text-gray-300 mb-3">
                        Aspects of consciousness by Murray Shanahan:
                    </p>
                    <div class="flex items-center space-x-4 text-gray-500 text-sm">
                         <button class="hover:text-blue-400"><i class="fas fa-comment-alt mr-1"></i> Reply</button>
                    </div>
                </div>

            </div>
        </main>

        <aside class="w-80 bg-gray-800 border-l border-gray-700 p-4 space-y-4 h-[calc(100vh-4rem)] sticky top-16 overflow-y-auto hidden md:block">
            <div class="trending-item-card">
                <div class="flex items-center justify-between mb-1">
                    <a href="#" class="text-blue-400 hover:underline font-semibold text-sm">nvidia/parakeet-tdt-0.6b-v2</a>
                    <span class="text-xs text-gray-500"><i class="fas fa-arrow-up text-green-500"></i> 167k+ <i class="fas fa-star text-yellow-400"></i> 874</span>
                </div>
                <p class="text-xs text-gray-400">Automatic Speech Recognition</p>
            </div>

            <div class="trending-item-card">
                 <div class="flex items-center justify-between mb-1">
                    <a href="#" class="text-blue-400 hover:underline font-semibold text-sm">DeepSite</a>
                    <span class="text-xs text-gray-500"><i class="fas fa-arrow-up text-green-500"></i> 5</span>
                </div>
                <p class="text-xs text-gray-400">Generate any application with DeepSeek</p>
            </div>

            <div class="trending-item-card">
                 <div class="flex items-center justify-between mb-1">
                    <a href="#" class="text-blue-400 hover:underline font-semibold text-sm">nari-labs/Dia-1.6B</a>
                     <span class="text-xs text-gray-500"><i class="fas fa-arrow-up text-green-500"></i> 17k+ <i class="fas fa-star text-yellow-400"></i> 2.1k</span>
                </div>
                <p class="text-xs text-gray-400">Text-to-Speech - Updated 3 d.</p>
            </div>

            <div class="trending-item-card">
                 <div class="flex items-center justify-between mb-1">
                    <a href="#" class="text-blue-400 hover:underline font-semibold text-sm">Computer Agent</a>
                </div>
                <p class="text-xs text-gray-400">Interact with an AI agent to perform web tasks</p>
            </div>
             <div class="trending-item-card">
                 <div class="flex items-center justify-between mb-1">
                    <a href="#" class="text-blue-400 hover:underline font-semibold text-sm">Lightricks/LTX-Video</a>
                     <span class="text-xs text-gray-500"><i class="fas fa-arrow-up text-green-500"></i> 201k+ <i class="fas fa-star text-yellow-400"></i> 1.49k</span>
                </div>
                <p class="text-xs text-gray-400">Text-to-Video - Updated 1 d.</p>
            </div>
             <div class="trending-item-card">
                 <div class="flex items-center justify-between mb-1">
                    <a href="#" class="text-blue-400 hover:underline font-semibold text-sm">DreamO</a>
                     <span class="text-xs text-gray-500"><i class="fas fa-arrow-up text-green-500"></i> 310</span>
                </div>
                <p class="text-xs text-gray-400">A Unified Framework for Image Customization</p>
            </div>


        </aside>
    </div>

<script>
    // Basic interactivity can be added here if needed, e.g., for tab switching.
    // For now, it's mostly a static representation.

    // Example: Sidebar active link
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Allow default navigation for actual links
            // For demo, just manage active state
            if (link.getAttribute('href') === '#') {
                 e.preventDefault();
            }

            sidebarLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Example: Main content tabs
    const mainContentTabs = document.querySelectorAll('.main-content-tab');
    mainContentTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            mainContentTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Example: Filter tabs in main content
    const filterTabs = document.querySelectorAll('nav[aria-label="Tabs"] a');
    filterTabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            filterTabs.forEach(t => {
                t.classList.remove('border-blue-500', 'text-blue-400');
                t.classList.add('border-transparent', 'text-gray-400', 'hover:text-gray-200', 'hover:border-gray-500');
            });
            this.classList.add('border-blue-500', 'text-blue-400');
            this.classList.remove('border-transparent', 'text-gray-400', 'hover:text-gray-200', 'hover:border-gray-500');
        });
    });

</script>
</body>
</html>
"""

notion_example = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notion - The AI workspace that works for you</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Simple custom font if needed, otherwise use tailwind defaults */
        body {
            font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
        }
    </style>
</head>
<body class="bg-white text-gray-800">
    <header class="container mx-auto px-6 py-4 flex items-center justify-between">
        <div class="flex items-center space-x-8">
            <div class="flex items-center space-x-2 text-lg font-semibold">
                <!-- TODO: Add SVG asset: Notion logo -->
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="24" height="24" fill="black"/>
                    <path d="M12 0C5.372 0 0 5.372 0 12C0 18.628 5.372 24 12 24C18.628 24 24 18.628 24 12C24 5.372 18.628 0 12 0ZM12 3C15.866 3 19 6.134 19 10V14C19 17.866 15.866 21 12 21C8.134 21 5 17.866 5 14V10C5 6.134 8.134 3 12 3Z" fill="white"/>
                </svg>
                <span>Notion</span>
            </div>
            <nav class="hidden md:flex items-center space-x-6 text-sm">
                <a href="#" class="hover:text-gray-900 flex items-center space-x-1">
                    <span>Notion</span>
                    <svg class="w-3 h-3 fill-current" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M4.516 7.548c.436-.446 1.043-.481 1.5-.149L10 10.66l3.984-3.261c.457-.332 1.064-.297 1.5.149.354.354.376.927.067 1.2-.297.288-5.429 4.525-5.429 4.525-.109.08-.248.12-.39.12s-.281-.04-.39-.12c0 0-5.132-4.237-5.429-4.525-.309-.273-.287-.846.067-1.2z"/></svg>
                </a>
                <a href="#" class="hover:text-gray-900 flex items-center space-x-1">
                    <span>Mail</span>
                    <span class="ml-1 text-xs font-medium bg-blue-500 text-white px-1.5 py-0.5 rounded">New</span>
                </a>
                <a href="#" class="hover:text-gray-900">Calendar</a>
                <a href="#" class="hover:text-gray-900">AI</a>
                <a href="#" class="hover:text-gray-900">Enterprise</a>
                <a href="#" class="hover:text-gray-900">Pricing</a>
                 <a href="#" class="hover:text-gray-900 flex items-center space-x-1">
                    <span>Explore</span>
                    <svg class="w-3 h-3 fill-current" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M4.516 7.548c.436-.446 1.043-.481 1.5-.149L10 10.66l3.984-3.261c.457-.332 1.064-.297 1.5.149.354.354.376.927.067 1.2-.297.288-5.429 4.525-5.429 4.525-.109.08-.248.12-.39.12s-.281-.04-.39-.12c0 0-5.132-4.237-5.429-4.525-.309-.273-.287-.846.067-1.2z"/></svg>
                </a>
                <a href="#" class="hover:text-gray-900">Request a demo</a>
            </nav>
        </div>
        <div class="flex items-center space-x-4">
            <a href="#" class="hidden md:inline-block hover:text-gray-900 text-sm">Log in</a>
            <button class="bg-black text-white text-sm font-medium px-4 py-2 rounded hover:opacity-90">Get Notion free</button>
        </div>
    </header>

    <main class="container mx-auto px-6 py-16 md:py-24 flex flex-col lg:flex-row items-center justify-between">
        <div class="w-full lg:w-1/2 mb-12 lg:mb-0 text-center lg:text-left">
            <h1 class="text-5xl md:text-7xl font-bold leading-tight mb-6">
                The AI workspace<br>that works for you.
            </h1>
            <p class="text-lg md:text-xl text-gray-700 mb-8">
                One place where teams find every answer, <br class="hidden md:inline">automate the busywork, and get projects done.
            </p>
            <div class="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4 justify-center lg:justify-start">
                <button class="bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-3 rounded-md text-lg">Get Notion free</button>
                <button class="bg-gray-100 hover:bg-gray-200 text-blue-600 font-medium px-6 py-3 rounded-md text-lg border border-gray-200">Request a demo</button>
            </div>
        </div>
        <div class="w-full lg:w-1/2 flex justify-center lg:justify-end">
            <!-- Placeholder for illustration -->
             <!-- TODO: Add SVG asset: Three abstract faces illustration -->
            <svg class="w-full max-w-md" viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg">
                <rect width="600" height="300" fill="#ffffff"/>
                <circle cx="150" cy="150" r="80" stroke="#e0e0e0" stroke-width="4" fill="none"/>
                <circle cx="300" cy="150" r="80" stroke="#e0e0e0" stroke-width="4" fill="none"/>
                <circle cx="450" cy="150" r="80" stroke="#e0e0e0" stroke-width="4" fill="none"/>
                <path d="M120 130 Q 150 100 180 130" stroke="black" stroke-width="4" fill="none"/>
                <circle cx="130" cy="110" r="8" fill="#ff4500"/>
                <circle cx="170" cy="110" r="8" fill="#ff4500"/>
                <path d="M130 120 C 135 125 165 125 170 120" stroke="#ff4500" stroke-width="4" fill="none"/>

                <path d="M270 130 Q 300 100 330 130" stroke="black" stroke-width="4" fill="none"/>
                <path d="M280 180 C 290 190 310 190 320 180" stroke="black" stroke-width="4" fill="none"/>
                <circle cx="340" cy="150" r="20" fill="#1a73e8"/>
                <path d="M320 140 C 350 120 380 140" stroke="black" stroke-width="4" fill="none"/>
                <path d="M330 160 C 360 180 390 160" stroke="black" stroke-width="4" fill="none"/>

                <path d="M420 130 Q 450 100 480 130" stroke="black" stroke-width="4" fill="none"/>
                 <path d="M430 180 C 440 190 460 190 470 180" stroke="black" stroke-width="4" fill="none"/>
            </svg>
        </div>
    </main>

    <section class="container mx-auto px-6 py-12 text-center">
        <p class="text-gray-500 text-sm mb-8">Trusted by top teams at</p>
        <div class="flex flex-wrap justify-center items-center gap-8 md:gap-12">
            <!-- TODO: Add SVG asset: OpenAI logo -->
            <svg width="100" height="24" viewBox="0 0 100 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="24" fill="white"/><text x="0" y="15" font-family="Arial" font-size="12" fill="black">OpenAI Logo Placeholder</text></svg>
             <!-- TODO: Add SVG asset: Figma logo -->
             <svg width="100" height="24" viewBox="0 0 100 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="24" fill="white"/><text x="0" y="15" font-family="Arial" font-size="12" fill="black">Figma Logo Placeholder</text></svg>
             <!-- TODO: Add SVG asset: Volvo logo -->
             <svg width="100" height="24" viewBox="0 0 100 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="24" fill="white"/><text x="0" y="15" font-family="Arial" font-size="12" fill="black">Volvo Logo Placeholder</text></svg>
             <!-- TODO: Add SVG asset: Ramp logo -->
             <svg width="100" height="24" viewBox="0 0 100 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="24" fill="white"/><text x="0" y="15" font-family="Arial" font-size="12" fill="black">Ramp Logo Placeholder</text></svg>
             <!-- TODO: Add SVG asset: Cursor logo -->
             <svg width="100" height="24" viewBox="0 0 100 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="24" fill="white"/><text x="0" y="15" font-family="Arial" font-size="12" fill="black">Cursor Logo Placeholder</text></svg>
             <!-- TODO: Add SVG asset: Headspace logo -->
             <svg width="100" height="24" viewBox="0 0 100 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="24" fill="white"/><text x="0" y="15" font-family="Arial" font-size="12" fill="black">Headspace Logo Placeholder</text></svg>
             <!-- TODO: Add SVG asset: Perplexity logo -->
             <svg width="100" height="24" viewBox="0 0 100 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="24" fill="white"/><text x="0" y="15" font-family="Arial" font-size="12" fill="black">Perplexity Logo Placeholder</text></svg>
             <!-- TODO: Add SVG asset: Vercel logo -->
             <svg width="100" height="24" viewBox="0 0 100 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="24" fill="white"/><text x="0" y="15" font-family="Arial" font-size="12" fill="black">Vercel Logo Placeholder</text></svg>
        </div>
    </section>

    <!-- Minimal JS not needed for this static layout -->

</body>
</html>
"""

system_prompt = """
You will be provided with a screenshot of a website to replicate **pixel-perfectly**.
Your output will be in HTML, Tailwind CSS, and minimal JavaScript for interactivity.
If you see assets in screenshots provided to you, including SVGs, just put placeholder images in the output and add a comment in the code TODO: Add image (resp. SVG) asset: <asset_description>.
Provide a description of the asset. If the asset is the same as a previous asset, use the exact same description. Make sure the placeholder has the same size and shape as the original asset.
If you see several similar items, e.g. screenshot of a page with a list of items, just design 2-3 items.
Focus on compact code and legibility.
Your output must be inside ```html ... ``` tags.
"""


def get_html_content(html_file_path):
    try:
        with open(html_file_path, encoding="utf-8") as f:
            html_content_data = f.read()
        return html_content_data
    except FileNotFoundError:
        return "<p>Error: HTML file not found. Please create a 'base.html' file.</p>"
    except Exception as e:
        return f"<p>An error occurred while reading HTML: {str(e)}</p>"


# --- Get your HTML content ---
actual_html_content = get_html_content("base.html")

custom_iframe_template = """
<iframe
    title="Embedded Application Content"
    srcdoc="{escaped_html_for_srcdoc}"
    style="width: 100%; height: 100%; min-height: 800px; border: none;"
    sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-modals allow-downloads allow-top-navigation-by-user-activation"
>
    <p>Your browser does not support iframes, or the embedded content could not be displayed.</p>
</iframe>
"""


def prepare_html_content(html_content: str):
    escaped_html_for_srcdoc = html_content.replace('"', "&quot;")
    html_content = custom_iframe_template.format(
        escaped_html_for_srcdoc=escaped_html_for_srcdoc
    )
    return html_content


cached_examples = ["screenshot_notion.png", "screenshot_hf.png"]

cached_examples_to_outputs = {
    "screenshot_notion.png": [prepare_html_content(notion_example), notion_example],
    "screenshot_hf.png": [prepare_html_content(hf_example), hf_example],
}

default_example_index = 0
default_example = cached_examples[default_example_index]
default_example_html, default_example_code = cached_examples_to_outputs[default_example]


def display_cached_examples(image_input):
    return cached_examples_to_outputs[image_input.split("/")[-1]]


# --- Chatbot Function (Example) ---
async def chat_function(message, history):
    history = history or []  # Ensure history is a list
    # Simulate a response
    response = f"Bot: I received '{message}'"
    history.append((message, response))
    return (
        history,
        "",
    )  # Return updated history for chatbot, and empty string to clear the textbox


def stream_code(image_input, gemini_api_key, model_name):
    gr.Info("Generating code from screenshot...")
    genai.configure(api_key=gemini_api_key)

    # Upload the image file
    image_file = genai.upload_file(image_input)

    # Create the model
    model = genai.GenerativeModel(model_name)

    contents = [
        few_shot_examples,
        system_prompt,
        "Screenshot of the website to replicate:",
        image_file,
    ]

    print("contents: ", contents)

    output = ""

    try:
        response = model.generate_content(contents, stream=True)
        for chunk in response:
            output += chunk.text
            yield gr.Code(value=output)
    except Exception as e:
        print("error: ", e)
        raise gr.Error(
            "Error when using Gemini API. Please retry later. Error:\n" + str(e)
        )

    print("output: ", output)
    gr.Success("Code generation complete")


def display_html(raw_output):
    print("--------------------------------")
    print("raw_output: ", raw_output)
    raw_html = extract_html_code(raw_output)

    print("--------------------------------")
    print("raw_html: ", raw_html)
    html_content = prepare_html_content(raw_html)
    return (
        gr.HTML(html_content),
        gr.Tabs(selected=0),
        gr.Code(value=raw_html, language="html"),
    )


def bot(history: list):
    response = "**That's cool!**"
    history.append({"role": "assistant", "content": ""})
    for character in response:
        history[-1]["content"] += character
        time.sleep(0.05)
        yield history


def clear(html_display, code_display):
    return gr.HTML(value=""), gr.Code(value="")


def check_key(gemini_api_key, model_name):
    if gemini_api_key == "":
        raise gr.Error("Gemini API Key is empty")

    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        model.generate_content("Hello, world!")
        gr.Success("Gemini API Key is valid")
        return gr.Code(value=""), gr.Tabs(selected=1)
    except Exception:
        raise gr.Error("Gemini API Key is invalid")


project_description = """
<h1 style="text-align: center;">📷 Screenshot to HTML</h1>

Easily turn mocks into HTML, or get started from an existing inspiring website.

📕 **Tutorial:**
- If you don't have a Gemini API Key, you can try with Gemini Flash *for free* on https://aistudio.google.com/app/apikey and enter it in the textbox.
- Upload a screenshot of the website you want to replicate.
- Click on the "Send" button to generate the HTML code.
- (Optional) Choose a model. Gemini Flash is **free** and fast to use, but for better results, use Gemini Pro.
- (Optional) Click on the "Examples" button to see the output of the code generated from sample screenshots.

⚠️ **Warnings:**
- Do not forget to put your Gemini API Key in the textbox.
- Gemini API often crashes

"""

# --- Gradio Interface ---
with gr.Blocks(theme=gr.themes.Default()) as demo:  # You can experiment with themes
    gemini_key_is_valid = gr.State(False)

    gr.Markdown(project_description)

    with gr.Row():
        with gr.Column(scale=2):  # 20%
            gr.Markdown("## Input")
            gemini_api_key = gr.Textbox(
                label="Gemini API Key",
                info="You can try with Gemini Flash *for free* on https://aistudio.google.com/app/apikey",
                value=api_key,
                interactive=True,
                type="password",
            )

            gr.Markdown("Input the screenshot to replicate into a HTML page here:")
            image_input = gr.Image(
                label="Screenshot",
                interactive=True,
                type="filepath",
                # value=default_example,
                visible=True,
            )
            with gr.Accordion("Model choice", open=False):
                model_name = gr.Dropdown(
                    label="Model Name",
                    value=supported_models[0],
                    interactive=True,
                    choices=supported_models,
                    info="Gemini Flash is free and fast to use, but for better results, use Gemini Pro.",
                )
            send_button = gr.Button(value="Send")
            clear_button = gr.Button(value="Reset")

        with gr.Column(scale=8):  # 80%
            gr.Markdown("## Output")
            with gr.Tabs(selected=0) as tab_group:
                with gr.Tab("HTML", id=0):
                    html_display = gr.HTML(
                        label="HTML Content",
                        value="The HTML code will be rendered here",
                    )
                with gr.Tab("Code", id=1):
                    code_display = gr.Code(
                        label="Code Content",
                        language="html",
                        value="The code will be rendered here",
                    )
    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown(
                "You can click on the examples below to see the output of the code generated from sample screenshots:"
            )
            # examples = gr.Examples(
            #         examples=cached_examples,
            #         inputs=image_input,
            #         outputs=[html_display, code_display],
            #         cache_examples=True,
            #         cache_mode="eager",
            #         fn = display_cached_examples,
            #
            # )
            gr.Markdown(
                "*Examples temporarily disabled - upload your own screenshot to test*"
            )
        with gr.Column(scale=8):
            gr.Textbox(visible=False)
    clear_fields = send_button.click(
        clear, [html_display, code_display], [html_display, code_display]
    )

    is_key_valid = clear_fields.then(
        check_key, [gemini_api_key, model_name], [code_display, tab_group]
    )

    code_streaming = is_key_valid.then(
        stream_code, [image_input, gemini_api_key, model_name], [code_display]
    )
    then_display_html = code_streaming.then(
        display_html, [code_display], [html_display, tab_group, code_display]
    )
    clear_button.click(
        clear, [html_display, code_display], [html_display, code_display]
    )

if __name__ == "__main__":
    import os

    # Configure for Docker deployment
    server_name = os.getenv("GRADIO_SERVER_NAME", "127.0.0.1")
    server_port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))

    demo.launch(
        server_name=server_name,
        server_port=server_port,
        debug=os.getenv("DEBUG", "false").lower() == "true",
    )

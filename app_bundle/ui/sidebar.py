def sidebar():
    return """
    <style>
        .sidebar {
            width: 260px;
            background: #1e1e1e;
            color: white;
            height: 100vh;
            position: fixed;
            left: 0;
            top: 0;
            padding: 20px;
            overflow-y: auto;
            transition: width 0.2s ease;
            border-right: 1px solid #333;
        }

        .sidebar.collapsed {
            width: 70px;
        }

        .sidebar h2 {
            margin-top: 0;
            font-size: 22px;
            text-align: center;
        }

        .sidebar ul {
            list-style: none;
            padding: 0;
        }

        .sidebar ul li {
            margin: 10px 0;
        }

        .sidebar ul li a {
            color: white;
            text-decoration: none;
            display: block;
            padding: 8px;
            border-radius: 4px;
        }

        .sidebar ul li a:hover {
            background: #333;
        }

        /* Search bar collapsed behavior */
        .sidebar.collapsed #sidebar-search {
            width: 40px !important;
            padding: 6px;
            font-size: 0;
        }

        .sidebar.collapsed #sidebar-search::placeholder {
            color: transparent;
        }

        .sidebar.collapsed #sidebar-search:focus {
            width: 180px !important;
            font-size: 14px;
        }

        /* Collapse button */
        #collapse-btn {
            background: #333;
            color: white;
            border: none;
            padding: 8px;
            width: 100%;
            border-radius: 4px;
            cursor: pointer;
            margin-bottom: 15px;
        }
    </style>

    <div class="sidebar" id="sidebar">

        <button id="collapse-btn" onclick="toggleSidebar()">☰ Menu</button>

        <!-- 🔍 SEARCH BAR -->
        <input
            type="text"
            id="sidebar-search"
            placeholder="Search tools..."
            onkeyup="filterSidebar()"
            style="
                width: 100%;
                padding: 8px;
                margin-bottom: 12px;
                border-radius: 4px;
                border: 1px solid #444;
                background: #2a2a2a;
                color: white;
            "
        >

        <ul>
            <li><a href="/admin/index" data-icon="🏠">🏠 Home</a></li>
            <li><a href="/admin/system" data-icon="💻">💻 System</a></li>
            <li><a href="/admin/processes" data-icon="⚙️">⚙️ Processes</a></li>
            <li><a href="/admin/network" data-icon="🌐">🌐 Network</a></li>
            <li><a href="/admin/services" data-icon="🛠️">🛠️ Services</a></li>
            <li><a href="/admin/security" data-icon="🔐">🔐 Security</a></li>
            <li><a href="/admin/firewall" data-icon="🔥">🔥 Firewall</a></li>
            <li><a href="/admin/storage" data-icon="💾">💾 Storage</a></li>
            <li><a href="/admin/logs" data-icon="📜">📜 Logs</a></li>
            <li><a href="/admin/metrics" data-icon="📊">📊 Metrics</a></li>
            <li><a href="/admin/performance" data-icon="🚀">🚀 Performance</a></li>
            <li><a href="/admin/kernel" data-icon="🧬">🧬 Kernel</a></li>
            <li><a href="/admin/hardware" data-icon="🖥️">🖥️ Hardware</a></li>
            <li><a href="/admin/packages" data-icon="📦">📦 Packages</a></li>
            <li><a href="/admin/config" data-icon="⚙️">⚙️ Config</a></li>
            <li><a href="/admin/audit" data-icon="🔍">🔍 Audit</a></li>
            <li><a href="/admin/events" data-icon="📡">📡 Events</a></li>
            <li><a href="/admin/tasks" data-icon="📌">📌 Tasks</a></li>
            <li><a href="/admin/scheduler" data-icon="⏱️">⏱️ Scheduler</a></li>
            <li><a href="/admin/threads" data-icon="🧵">🧵 Threads</a></li>
            <li><a href="/admin/timers" data-icon="⏲️">⏲️ Timers</a></li>
            <li><a href="/admin/locks" data-icon="🔒">🔒 Locks</a></li>
            <li><a href="/admin/signals" data-icon="📶">📶 Signals</a></li>
            <li><a href="/admin/deadlock" data-icon="💀">💀 Deadlock</a></li>
            <li><a href="/admin/cache" data-icon="🧊">🧊 Cache</a></li>
            <li><a href="/admin/sockets" data-icon="🔌">🔌 Sockets</a></li>
            <li><a href="/admin/runtime" data-icon="⏳">⏳ Runtime</a></li>
            <li><a href="/admin/env" data-icon="🌱">🌱 Environment</a></li>
            <li><a href="/admin/limits" data-icon="📉">📉 Limits</a></li>
            <li><a href="/admin/paths" data-icon="📁">📁 Paths</a></li>
            <li><a href="/admin/inspect" data-icon="🔎">🔎 Inspect</a></li>
            <li><a href="/admin/async_panel" data-icon="⚡">⚡ Async</a></li>
        </ul>
    </div>

    <script>
        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            sidebar.classList.toggle('collapsed');
            localStorage.setItem('sidebar-collapsed', sidebar.classList.contains('collapsed'));
        }

        // Restore collapsed state
        window.onload = () => {
            const sidebar = document.getElementById('sidebar');
            if (localStorage.getItem('sidebar-collapsed') === 'true') {
                sidebar.classList.add('collapsed');
            }
        };

        // 🔍 Search filter logic
        function filterSidebar() {
            const input = document.getElementById('sidebar-search');
            const filter = input.value.toLowerCase();
            const links = document.querySelectorAll('.sidebar ul li a');

            links.forEach(link => {
                const text = link.textContent.toLowerCase();
                const icon = link.getAttribute('data-icon')?.toLowerCase() || "";

                if (text.includes(filter) || icon.includes(filter)) {
                    link.parentElement.style.display = "";
                } else {
                    link.parentElement.style.display = "none";
                }
            });
        }
    </script>
    """

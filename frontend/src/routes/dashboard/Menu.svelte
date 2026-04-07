<script>
    import { page } from "$app/stores";

    const links = [
        { label: "Dashboard", href: "/dashboard" },
        { label: "PELM", href: "/dashboard?panel=pelm" },
        { label: "System", href: "/dashboard?panel=system" },
        { label: "IDRIM", href: "/dashboard?panel=idrim" }
    ];

    $: current = $page.url.pathname + $page.url.search;
</script>

<style>
    nav {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        padding: 1rem;
        background: var(--panel-bg);
        border-right: 1px solid var(--border);
        min-width: 200px;
    }

    a {
        padding: 0.5rem 0.75rem;
        border-radius: 6px;
        text-decoration: none;
        color: var(--text);
        font-weight: 500;
        transition: background 0.15s ease;
    }

    a:hover {
        background: var(--hover-bg);
    }

    .active {
        background: var(--accent-bg);
        color: var(--accent-text);
    }
</style>

<nav>
    {#each links as link}
        <a
            href={link.href}
            class:selected={current.startsWith(link.href)}
            class:active={current.startsWith(link.href)}
        >
            {link.label}
        </a>
    {/each}
</nav>

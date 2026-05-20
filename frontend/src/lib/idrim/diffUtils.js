// frontend/src/lib/idrim/diffUtils.js

export function formatDiffSection(section) {
    return [
        ...Object.entries(section.added).map(([k, v]) => ({
            type: "added",
            key: k,
            value: v
        })),
        ...Object.entries(section.removed).map(([k, v]) => ({
            type: "removed",
            key: k,
            value: v
        })),
        ...Object.entries(section.changed).map(([k, v]) => ({
            type: "changed",
            key: k,
            before: v.before,
            after: v.after
        }))
    ];
}

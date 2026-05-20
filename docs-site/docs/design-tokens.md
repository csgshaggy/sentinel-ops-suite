# Design Tokens

These tokens are synced from the dashboard source of truth:

`frontend/dashboard/design-tokens/figma-tokens.json`

They are automatically copied into:

`docs-site/docs/assets/design-tokens/figma-tokens.json`

Below is a live-rendered table of all tokens.

<script setup>
import { ref, onMounted } from 'vue'

const tokens = ref([])

onMounted(async () => {
  const res = await fetch('/assets/design-tokens/figma-tokens.json')
  const json = await res.json()

  const flat = []

  const walk = (obj, prefix = '') => {
    for (const key in obj) {
      const value = obj[key]
      const path = prefix ? `${prefix}.${key}` : key

      if (typeof value === 'object' && !value.value) {
        walk(value, path)
      } else if (value && typeof value === 'object' && 'value' in value) {
        flat.push({
          name: path,
          value: value.value,
          type: value.type || 'unknown'
        })
      }
    }
  }

  walk(json)
  tokens.value = flat
})
</script>

<table>
  <thead>
    <tr>
      <th style="text-align:left;">Token</th>
      <th style="text-align:left;">Value</th>
      <th style="text-align:left;">Type</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="t in tokens" :key="t.name">
      <td>{{ t.name }}</td>
      <td>{{ t.value }}</td>
      <td>{{ t.type }}</td>
    </tr>
  </tbody>
</table>

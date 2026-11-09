<template>
  <div v-if="show" class="modal" tabindex="-1" @click.self="$emit('close')">
    <div class="modal-dialog modal-lg modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title d-flex align-items-center flex-wrap gap-2">
            <em>{{ lemma }}</em>
            <span v-if="pos" class="badge bg-secondary align-middle">{{ pos }}</span>
            <span class="text-muted fs-6">muutokšet</span>
          </h5>
          <button type="button" class="btn-close" @click="$emit('close')" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div v-if="loading" class="text-muted">…</div>
          <div v-else-if="error" class="alert alert-warning mb-0">{{ error }}</div>

          <!-- Глагол: секции по наклонению / блоку -->
          <div v-else-if="isVerb">
            <section v-for="sec in verbSections" :key="sec.id" class="paradigm-section mb-3">
              <h6 class="section-title">{{ sec.title }}</h6>
              <table class="table table-sm table-bordered mb-0">
                <tbody>
                  <tr
                    v-for="row in sec.rows"
                    :key="row.code"
                    :class="{ 'form-highlight': isHighlighted(row.form) }"
                  >
                    <td class="label-cell" :title="row.name_ru">{{ row.name_krl }}</td>
                    <td class="form-cell"><em>{{ row.form }}</em></td>
                  </tr>
                </tbody>
              </table>
            </section>
          </div>

          <!-- Имя / прилагательное / местоимение: ед. / мн. -->
          <div v-else class="row">
            <div v-if="sgForms.length" class="col-md-6 mb-3">
              <h6 class="text-muted">Yksikkö</h6>
              <table class="table table-sm table-bordered mb-0">
                <tbody>
                  <tr
                    v-for="row in sgForms"
                    :key="row.code"
                    :class="{ 'form-highlight': isHighlighted(row.form) }"
                  >
                    <td class="label-cell" :title="row.name_ru">{{ row.name_krl }}</td>
                    <td class="form-cell"><em>{{ row.form }}</em></td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-if="plForms.length" class="col-md-6 mb-3">
              <h6 class="text-muted">Monikko</h6>
              <table class="table table-sm table-bordered mb-0">
                <tbody>
                  <tr
                    v-for="row in plForms"
                    :key="row.code"
                    :class="{ 'form-highlight': isHighlighted(row.form) }"
                  >
                    <td class="label-cell" :title="row.name_ru">{{ row.name_krl }}</td>
                    <td class="form-cell"><em>{{ row.form }}</em></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';

/** Порядок и заголовки секций глагола (по префиксу code). */
const VERB_SECTION_DEFS = [
  { id: 'ind_pres', title: 'Indikativa — prezens', match: (c) => c.startsWith('ind_pres_') },
  { id: 'ind_impf', title: 'Indikativa — imperfekta', match: (c) => c.startsWith('ind_impf_') },
  { id: 'ind_perf', title: 'Indikativa — perfekta', match: (c) => c.startsWith('ind_perf_') },
  { id: 'ind_plup', title: 'Indikativa — pluskvamperfekta', match: (c) => c.startsWith('ind_plup_') },
  { id: 'imp', title: 'Imperativa', match: (c) => c.startsWith('imp_') },
  { id: 'cond_impf', title: 'Konditsionala — imperfekta', match: (c) => c.startsWith('cond_impf_') },
  { id: 'cond_perf', title: 'Konditsionala — perfekta', match: (c) => c.startsWith('cond_perf_') },
  { id: 'cond_plup', title: 'Konditsionala — pluskvamperfekta', match: (c) => c.startsWith('cond_plup_') },
  { id: 'pot_pres', title: 'Potentiala — prezens', match: (c) => c.startsWith('pot_pres_') },
  { id: 'pot_perf', title: 'Potentiala — perfekta', match: (c) => c.startsWith('pot_perf_') },
  {
    id: 'inf',
    title: 'Infinitivat',
    match: (c) => c === 'inf1' || c.startsWith('inf2_') || c.startsWith('inf3_'),
  },
  { id: 'part', title: 'Partisiipat', match: (c) => c.startsWith('part_') },
];

export default {
  name: 'ParadigmPopup',
  props: {
    show: { type: Boolean, required: true },
    lemma: { type: String, default: '' },
    pos: { type: String, default: '' },
    highlightForm: { type: String, default: '' },
    forms: { type: Array, default: () => [] },
    loading: { type: Boolean, default: false },
    error: { type: String, default: '' },
  },
  emits: ['close'],
  setup(props) {
    const isVerb = computed(() => {
      if (props.pos === 'v.') return true;
      // Явный именной/местоимённый POS — не глагол (part_sg ≠ partisiippa).
      if (props.pos) return false;
      // fallback без pos: только явно глагольные коды
      return props.forms.some((f) =>
        /^(ind_|imp_|cond_|pot_|inf\d|inf[23]_|part_(pres|perf|act|pass))/.test(f.code)
      );
    });

    const sgForms = computed(() => props.forms.filter((f) => f.number === 'sg'));
    const plForms = computed(() => props.forms.filter((f) => f.number === 'pl'));

    const verbSections = computed(() => {
      const used = new Set();
      const sections = [];
      for (const def of VERB_SECTION_DEFS) {
        const rows = props.forms.filter((f) => def.match(f.code));
        if (!rows.length) continue;
        rows.forEach((r) => used.add(r.code));
        sections.push({ id: def.id, title: def.title, rows });
      }
      const rest = props.forms.filter((f) => !used.has(f.code));
      if (rest.length) {
        sections.push({ id: 'other', title: 'Muut', rows: rest });
      }
      return sections;
    });

    const isHighlighted = (cellForm) => {
      const needle = (props.highlightForm || '').trim().toLowerCase();
      if (!needle || !cellForm) return false;
      return String(cellForm)
        .split(/\s*\/\s*/)
        .some((part) => part.trim().toLowerCase() === needle);
    };

    return { isVerb, sgForms, plForms, verbSections, isHighlighted };
  },
};
</script>

<style scoped>
.modal {
  display: block;
  background: rgba(0, 0, 0, 0.45);
  position: fixed;
  inset: 0;
  z-index: 1050;
}
.modal-dialog {
  margin: 1.75rem auto;
}
.label-cell {
  font-size: 0.85rem;
  color: #555;
  width: 55%;
}
.form-cell {
  font-size: 1rem;
}
.section-title {
  color: #6c757d;
  font-size: 0.95rem;
  margin-bottom: 0.35rem;
  border-bottom: 1px solid #dee2e6;
  padding-bottom: 0.2rem;
}
.paradigm-section:last-child {
  margin-bottom: 0 !important;
}
.table > tbody > tr.form-highlight > td {
  background-color: #fff3cd !important;
}
.table > tbody > tr.form-highlight .form-cell {
  font-weight: 600;
}
</style>

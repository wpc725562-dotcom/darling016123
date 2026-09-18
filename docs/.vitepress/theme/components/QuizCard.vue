<script setup>
import { ref, computed, watch } from 'vue'
import { questions as computerQuestions } from './quiz-computer'
import { questions as mathQuestions } from './quiz-math'
import { questions as englishQuestions } from './quiz-english'

const props = defineProps({
  subject: { type: String, required: true },
  /** 初始筛选的章节号，如 '1.8'（指针）。留空 = 全部 */
  chapter: { type: String, default: '' },
  /** 一次出多少题（随机抽）；0 = 全部 */
  limit: { type: Number, default: 0 },
})

const bank = {
  computer: computerQuestions,
  math: mathQuestions,
  english: englishQuestions,
}
const all = bank[props.subject] || []

/* ---------- 考点筛选 ---------- */
const chapters = computed(() => {
  const m = new Map()
  for (const q of all) {
    const key = q.chapter || ''
    if (!key) continue
    const cur = m.get(key) || { key, label: q.point || key, n: 0 }
    cur.n++
    m.set(key, cur)
  }
  return [...m.values()].sort((a, b) => a.key.localeCompare(b.key, undefined, { numeric: true }))
})

const filter = ref(props.chapter || '')
watch(() => props.chapter, (v) => { filter.value = v || ''; restart() })

const pool = computed(() => (filter.value ? all.filter((q) => q.chapter === filter.value) : all))

/* ---------- 状态 ---------- */
const order = ref([])
const idx = ref(0)
const selected = ref(null)
const revealed = ref(false)
const finished = ref(false)
const answers = ref([])

function buildOrder() {
  const list = pool.value.slice()
  if (props.limit > 0 && props.limit < list.length) {
    for (let i = list.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1))
      ;[list[i], list[j]] = [list[j], list[i]]
    }
    return list.slice(0, props.limit)
  }
  return list
}
function restart() {
  order.value = buildOrder()
  idx.value = 0
  selected.value = null
  revealed.value = false
  finished.value = false
  answers.value = []
}
restart()

const current = computed(() => order.value[idx.value] || null)
const score = computed(() => answers.value.filter((a) => a.ok).length)
const wrong = computed(() => answers.value.filter((a) => !a.ok))
const letters = ['A', 'B', 'C', 'D']
const total = computed(() => order.value.length)

function optionText(o) {
  return String(o).replace(/^[A-D][.、:：]\s*/, '')
}
function choose(i) {
  if (revealed.value || finished.value) return
  selected.value = i
}
function reveal() {
  if (selected.value === null || revealed.value) return
  revealed.value = true
  answers.value.push({
    q: current.value.q,
    picked: selected.value,
    correct: current.value.answer,
    ok: selected.value === current.value.answer,
    explain: current.value.explain,
    point: current.value.point,
    year: current.value.year,
  })
}
function next() {
  if (idx.value + 1 < total.value) {
    idx.value++
    selected.value = null
    revealed.value = false
  } else {
    finished.value = true
  }
}
function prev() {
  if (idx.value > 0) {
    idx.value--
    selected.value = null
    revealed.value = false
    answers.value.pop()
  }
}
function retryWrong() {
  const w = wrong.value
  if (!w.length) return
  order.value = w.map((a) => all.find((q) => q.q === a.q)).filter(Boolean)
  idx.value = 0
  selected.value = null
  revealed.value = false
  finished.value = false
  answers.value = []
}
</script>

<template>
  <div class="quiz-card">
    <p v-if="all.length === 0" class="quiz-empty">题库数据缺失，请稍后重试。</p>

    <template v-else-if="!finished">
      <div class="quiz-bar">
        <div class="quiz-progress">
          <span>第 {{ idx + 1 }} / {{ total }} 题</span>
          <span v-if="current.kind === '判断'" class="quiz-tag">判断题</span>
          <span v-if="current.year && current.year !== '热身'" class="quiz-tag">{{ current.year }}</span>
          <span class="quiz-score">答对 {{ score }}</span>
        </div>
        <select v-if="chapters.length" v-model="filter" class="quiz-select" @change="restart">
          <option value="">全部考点（{{ all.length }} 题）</option>
          <option v-for="c in chapters" :key="c.key" :value="c.key">
            {{ c.label }}（{{ c.n }} 题）
          </option>
        </select>
      </div>

      <h3 class="quiz-q">{{ current.q }}</h3>
      <ul class="quiz-opts">
        <li v-for="(opt, i) in current.options" :key="i">
          <button
            class="quiz-opt"
            :class="{
              'is-selected': selected === i,
              'is-correct': revealed && i === current.answer,
              'is-wrong': revealed && selected === i && i !== current.answer,
            }"
            @click="choose(i)"
          >
            <span class="quiz-letter">{{ letters[i] }}.</span>
            <span>{{ optionText(opt) }}</span>
          </button>
        </li>
      </ul>
      <div class="quiz-actions">
        <button class="quiz-btn" :disabled="selected === null || revealed" @click="reveal">查看答案</button>
        <button class="quiz-btn" :disabled="idx === 0" @click="prev">上一题</button>
        <button class="quiz-btn quiz-btn-primary" @click="next">
          {{ idx + 1 < total ? '下一题' : '交卷' }}
        </button>
      </div>
      <div v-if="revealed" class="quiz-explain">
        <p class="quiz-ans">
          <template v-if="selected === current.answer">✅ 答对了 · </template>
          <template v-else>❌ 答错了 · </template>
          正确答案：<b>{{ letters[current.answer] }}</b>
          <span v-if="current.point" class="quiz-point">考点 {{ current.point }}</span>
        </p>
        <p v-if="current.explain" class="quiz-exp-text">{{ current.explain }}</p>
      </div>
    </template>

    <div v-else class="quiz-result">
      <h3>🎉 完成！</h3>
      <p class="quiz-score-big">
        得分 <b>{{ score }}</b> / {{ answers.length }}
        <span class="quiz-pct">{{ answers.length ? Math.round((score / answers.length) * 100) : 0 }}%</span>
      </p>

      <div v-if="wrong.length" class="quiz-wrongbox">
        <h4>❌ 错题 {{ wrong.length }} 道 —— 这几道才是真正该复习的</h4>
        <ol class="quiz-wronglist">
          <li v-for="(w, i) in wrong" :key="i">
            <p class="quiz-wq">{{ w.q }}</p>
            <p class="quiz-wmeta">
              你选 <b class="bad">{{ letters[w.picked] }}</b> ·
              正确 <b class="good">{{ letters[w.correct] }}</b>
              <span v-if="w.point" class="quiz-point">考点 {{ w.point }}</span>
            </p>
            <p v-if="w.explain" class="quiz-wexp">{{ w.explain }}</p>
          </li>
        </ol>
      </div>
      <p v-else class="quiz-perfect">全对！这一组可以过了。</p>

      <div class="quiz-actions quiz-actions-center">
        <button v-if="wrong.length" class="quiz-btn" @click="retryWrong">只重做错题</button>
        <button class="quiz-btn quiz-btn-primary" @click="restart">重新开始</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.quiz-card {
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 20px;
  margin: 16px 0;
  background: var(--vp-c-bg-soft);
}
.quiz-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 10px;
}
.quiz-progress {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--vp-c-text-2);
}
.quiz-tag {
  padding: 1px 7px;
  border-radius: 999px;
  border: 1px solid var(--vp-c-divider);
  font-size: 11.5px;
}
.quiz-score { color: var(--vp-c-brand-1); font-weight: 600; }
.quiz-select {
  padding: 6px 10px;
  border-radius: 8px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 13px;
  max-width: 100%;
}
.quiz-q { font-size: 16px; line-height: 1.6; margin: 8px 0 12px; }
.quiz-opts {
  list-style: none;
  padding: 0;
  margin: 0 0 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.quiz-opt {
  width: 100%;
  text-align: left;
  display: flex;
  gap: 8px;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  cursor: pointer;
  font-size: 14px;
  line-height: 1.5;
}
.quiz-opt:hover { border-color: var(--vp-c-brand-1); }
.quiz-opt.is-selected { border-color: var(--vp-c-brand-1); background: var(--vp-c-brand-soft); }
.quiz-opt.is-correct { border-color: #22c55e; background: rgba(34, 197, 94, 0.12); }
.quiz-opt.is-wrong { border-color: #ef4444; background: rgba(239, 68, 68, 0.12); }
.quiz-letter { font-weight: 600; color: var(--vp-c-brand-1); }
.quiz-actions { display: flex; gap: 8px; flex-wrap: wrap; }
.quiz-actions-center { justify-content: center; margin-top: 14px; }
.quiz-btn {
  padding: 8px 14px;
  border-radius: 8px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  cursor: pointer;
  font-size: 14px;
}
.quiz-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.quiz-btn-primary { background: var(--vp-c-brand-1); border-color: var(--vp-c-brand-1); color: #fff; }
.quiz-explain {
  margin-top: 12px;
  padding: 10px 12px;
  border-radius: 8px;
  background: var(--vp-c-brand-soft);
  font-size: 14px;
}
.quiz-ans { margin: 0 0 6px; }
/* ★ pre-line 必须留着：真题解析里常有编号步骤（1. mid = … 2. mid = …），
   默认 white-space 会把换行折叠成空格，步骤全挤成一坨。 */
.quiz-exp-text { margin: 0; line-height: 1.65; color: var(--vp-c-text-2); white-space: pre-line; }
.quiz-point {
  margin-left: 8px;
  font-size: 12px;
  padding: 1px 7px;
  border-radius: 999px;
  background: var(--vp-c-default-soft);
  color: var(--vp-c-text-2);
}
.quiz-result { text-align: center; padding: 8px 0; }
.quiz-score-big { font-size: 18px; margin: 8px 0 16px; }
.quiz-pct { color: var(--vp-c-brand-1); font-weight: 600; margin-left: 6px; }
.quiz-perfect { color: var(--vp-c-brand-1); }
.quiz-wrongbox {
  text-align: left;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  padding: 14px 16px;
  background: var(--vp-c-bg);
  margin-bottom: 8px;
}
.quiz-wrongbox h4 { margin: 0 0 10px; font-size: 14.5px; }
.quiz-wronglist { margin: 0; padding-left: 20px; }
.quiz-wronglist li { margin-bottom: 14px; }
.quiz-wq { margin: 0 0 4px; font-size: 14px; line-height: 1.55; }
.quiz-wmeta { margin: 0; font-size: 13px; color: var(--vp-c-text-2); }
.quiz-wmeta .bad { color: #ef4444; }
.quiz-wmeta .good { color: #22c55e; }
.quiz-wexp { margin: 4px 0 0; font-size: 13px; color: var(--vp-c-text-2); line-height: 1.6; white-space: pre-line; }
.quiz-empty { color: var(--vp-c-text-2); }
</style>

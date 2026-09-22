<template>
  <div
    class="live2d-controls"
    :style="{ '--live2d-control-bottom': `${controlBottom}px` }"
  >
    <button
      v-if="loaded && !disabled"
      class="live2d-close"
      type="button"
      aria-label="关闭看板娘"
      title="关闭看板娘"
      @click="disableWidget"
    >×</button>
    <details
      v-if="loaded && !disabled"
      class="live2d-size-menu"
    >
      <summary
        aria-label="调整看板娘大小"
        title="调整看板娘大小"
      ><span aria-hidden="true">↕</span></summary>
      <div
        class="live2d-size-popover"
        role="group"
        aria-label="看板娘大小调节"
      >
        <button
          class="live2d-size-step live2d-size-minus"
          type="button"
          aria-label="缩小看板娘"
          :disabled="sizePercent <= SIZE_MIN"
          @click="adjustSize(-SIZE_STEP)"
        >−</button>
        <input
          v-model.number="sizePercent"
          class="live2d-size-slider"
          type="range"
          :min="SIZE_MIN"
          :max="SIZE_MAX"
          :step="SIZE_STEP"
          aria-label="看板娘大小"
          :aria-valuetext="`${sizePercent}%`"
          @input="applyWidgetSize()"
        >
        <button
          class="live2d-size-step live2d-size-plus"
          type="button"
          aria-label="放大看板娘"
          :disabled="sizePercent >= SIZE_MAX"
          @click="adjustSize(SIZE_STEP)"
        >＋</button>
        <button
          class="live2d-size-value"
          type="button"
          aria-label="恢复看板娘默认大小"
          title="恢复默认大小"
          @click="resetSize"
        >{{ sizePercent }}%</button>
      </div>
    </details>
    <button
      v-else-if="disabled && desktopEligible"
      class="live2d-restore"
      type="button"
      title="显示看板娘"
      @click="restoreWidget"
    >🌸 看板娘</button>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { withBase } from 'vitepress'

const MODEL_PATH = withBase('/live2d/model.json')
const STORAGE_KEY = 'zsb-live2d-disabled'
const SIZE_STORAGE_KEY = 'zsb-live2d-size'
const BASE_WIDTH = 200
const BASE_HEIGHT = 300
const SIZE_MIN = 70
const SIZE_MAX = 150
const SIZE_STEP = 5
const DEFAULT_SIZE = 80
const loaded = ref(false)
const disabled = ref(false)
const desktopEligible = ref(false)
const sizePercent = ref(DEFAULT_SIZE)
const controlBottom = computed(() => Math.round(BASE_HEIGHT * sizePercent.value / 100 - 14))
let loadTimer: ReturnType<typeof setTimeout> | null = null
let idleHandle: number | null = null
let sizeApplyFrame: number | null = null

type IdleWindow = Window & {
  requestIdleCallback?: (callback: () => void, options?: { timeout: number }) => number
  cancelIdleCallback?: (handle: number) => void
}

declare global {
  interface Window {
    L2Dwidget: any
  }
}

async function loadResources(): Promise<void> {
  // Font Awesome（live2d-widget 依赖）
  if (!document.querySelector('link[data-live2d="fa"]')) {
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = withBase('/live2d/font-awesome.min.css')
    link.setAttribute('data-live2d', 'fa')
    document.head.appendChild(link)
  }

  // L2Dwidget JS（已本地化，不依赖 CDN）
  if (!window.L2Dwidget) {
    await new Promise<void>((resolve, reject) => {
      const script = document.createElement('script')
      script.src = withBase('/live2d/L2Dwidget.min.js')
      script.onload = () => resolve()
      script.onerror = () => reject(new Error('Live2D load failed'))
      document.head.appendChild(script)
    })
  }
}

function initWidget(): void {
  // L2Dwidget 的 webpack public path 已调整为根域名下的 /live2d/，
  // 会自动从本地加载 chunk (L2Dwidget.0.min.js) 与模型资源。
  window.L2Dwidget.init({
    tagMode: false,
    debug: false,
    model: {
      jsonPath: MODEL_PATH,
      scale: 1,
    },
    display: {
      superSample: 2,
      width: BASE_WIDTH,
      height: BASE_HEIGHT,
      position: 'left',
      hOffset: -16,
      vOffset: -10,
    },
    mobile: {
      show: false,
      scale: 0.5,
      motion: false,
    },
    react: {
      // ★ 2026-09-22：0.8 → 0.5。1023px 视口下 0.8 明显压住卡片内容。
      //   opacityOnHover 与 pointer-events:none 冲突（不触发），保持同值避免误解。
      opacityDefault: 0.5,
      opacityOnHover: 0.5,
    },
    dialog: {
      enable: false,
      hitokoto: false,
    },
    name: {
      canvas: 'live2dcanvas',
      div: 'live2d-widget',
    },
    dev: {
      border: false,
    },
  })
  loaded.value = true
  scheduleWidgetSize()
}

function normalizeSize(value: number): number {
  const safeValue = Number.isFinite(value) ? value : DEFAULT_SIZE
  const clamped = Math.min(SIZE_MAX, Math.max(SIZE_MIN, safeValue))
  return Math.round(clamped / SIZE_STEP) * SIZE_STEP
}

function readStoredSize(): number {
  const stored = Number(localStorage.getItem(SIZE_STORAGE_KEY))
  return stored ? normalizeSize(stored) : DEFAULT_SIZE
}

function applyWidgetSize(persist = true): boolean {
  sizePercent.value = normalizeSize(sizePercent.value)
  const canvas = document.getElementById('live2dcanvas')
  if (persist) localStorage.setItem(SIZE_STORAGE_KEY, String(sizePercent.value))
  if (!canvas) return false
  // 旧版 L2Dwidget 在 superSample > 1 时不会为 CSS 尺寸补 px，
  // 显式固定显示尺寸，既保留高清画布，也避免视觉尺寸翻倍。
  canvas.style.width = `${BASE_WIDTH}px`
  canvas.style.height = `${BASE_HEIGHT}px`
  canvas.style.transformOrigin = 'left bottom'
  canvas.style.transition = 'transform 180ms ease'
  canvas.style.transform = `scale(${sizePercent.value / 100})`
  // ★ 2026-09-22：看板娘是装饰，不该吃掉下层卡片的点击。
  //   1023px 视口下它压在「政治真题」卡片上，导致该入口点不进去。
  canvas.style.pointerEvents = 'none'
  const box = document.getElementById('live2d-widget') || canvas.parentElement
  if (box) box.style.pointerEvents = 'none'
  return true
}

function scheduleWidgetSize(attempt = 0): void {
  if (applyWidgetSize(false) || attempt >= 120) {
    sizeApplyFrame = null
    return
  }
  sizeApplyFrame = requestAnimationFrame(() => scheduleWidgetSize(attempt + 1))
}

function adjustSize(change: number): void {
  sizePercent.value = normalizeSize(sizePercent.value + change)
  applyWidgetSize()
}

function resetSize(): void {
  sizePercent.value = DEFAULT_SIZE
  localStorage.removeItem(SIZE_STORAGE_KEY)
  applyWidgetSize(false)
}

function shouldLoad(): boolean {
  const connection = (navigator as Navigator & { connection?: { saveData?: boolean } }).connection
  return window.matchMedia('(min-width: 900px) and (prefers-reduced-motion: no-preference)').matches
    && !connection?.saveData
}

async function loadWidget(): Promise<void> {
  if (disabled.value || loaded.value) return
  try {
    await loadResources()
    initWidget()
  } catch (e) {
    console.error('Live2D load failed:', e)
  }
}

function setWidgetVisible(visible: boolean): boolean {
  // 兼容修复前错误使用的 live2d-tooltip 容器 ID。
  const widget = document.getElementById('live2d-widget')
    || document.getElementById('live2d-tooltip')
    || document.getElementById('live2dcanvas')?.parentElement
  if (!widget) return false
  widget.style.display = visible ? '' : 'none'
  return true
}

function disableWidget(): void {
  disabled.value = true
  localStorage.setItem(STORAGE_KEY, '1')
  // L2Dwidget 没有可靠的销毁 API。保留已初始化实例，仅隐藏画布，
  // 避免恢复时重复创建 WebGL 上下文导致花屏。
  setWidgetVisible(false)
}

function restoreWidget(): void {
  disabled.value = false
  localStorage.removeItem(STORAGE_KEY)
  if (setWidgetVisible(true)) {
    loaded.value = true
    scheduleWidgetSize()
    return
  }
  void loadWidget()
}

onMounted(() => {
  sizePercent.value = readStoredSize()
  desktopEligible.value = shouldLoad()
  disabled.value = localStorage.getItem(STORAGE_KEY) === '1'
  if (!desktopEligible.value || disabled.value) return

  // 浏览器空闲时再加载 1MB+ 的模型；不支持 idle callback 时延迟加载。
  const idleWindow = window as IdleWindow
  if (idleWindow.requestIdleCallback) {
    idleHandle = idleWindow.requestIdleCallback(() => {
      void loadWidget()
    }, { timeout: 5000 })
  } else {
    loadTimer = setTimeout(() => {
      void loadWidget()
    }, 3000)
  }
})

onUnmounted(() => {
  if (loadTimer) clearTimeout(loadTimer)
  if (sizeApplyFrame !== null) cancelAnimationFrame(sizeApplyFrame)
  if (idleHandle !== null) {
    const idleWindow = window as IdleWindow
    idleWindow.cancelIdleCallback?.(idleHandle)
  }
})
</script>

<style scoped>
.live2d-close,
.live2d-restore,
.live2d-size-menu > summary,
.live2d-size-popover {
  border: 1px solid var(--vp-c-divider);
  background: color-mix(in srgb, var(--vp-c-bg) 88%, transparent);
  color: var(--vp-c-text-2);
  box-shadow: 0 4px 16px rgba(0, 0, 0, .1);
  backdrop-filter: blur(10px);
}
.live2d-close,
.live2d-restore {
  position: fixed;
  left: 16px;
  z-index: 100001;
  cursor: pointer;
}
.live2d-close {
  bottom: var(--live2d-control-bottom, 286px);
  width: 30px;
  height: 30px;
  border-radius: 50%;
  font-size: 20px;
  line-height: 1;
}
.live2d-restore {
  bottom: 18px;
  padding: 7px 11px;
  border-radius: 999px;
  font-size: 12px;
}
.live2d-size-menu {
  position: fixed;
  left: 16px;
  bottom: calc(var(--live2d-control-bottom, 286px) - 36px);
  z-index: 100001;
}
.live2d-size-menu > summary {
  display: grid;
  width: 30px;
  height: 30px;
  place-items: center;
  border-radius: 50%;
  font-size: 15px;
  line-height: 1;
  list-style: none;
  cursor: pointer;
  user-select: none;
}
.live2d-size-menu > summary::-webkit-details-marker { display: none; }
.live2d-size-menu[open] > summary {
  color: var(--accent-color);
  border-color: var(--sakura-pink);
}
.live2d-size-popover {
  position: absolute;
  left: 38px;
  bottom: 0;
  display: grid;
  grid-template-columns: 26px 86px 26px;
  grid-template-areas:
    "minus slider plus"
    ". value .";
  gap: 5px 7px;
  width: 166px;
  padding: 8px;
  border-radius: 12px;
}
.live2d-size-step,
.live2d-size-value {
  border: 0;
  color: var(--vp-c-text-1);
  background: color-mix(in srgb, var(--sakura-pink) 18%, transparent);
  cursor: pointer;
}
.live2d-size-step {
  width: 26px;
  height: 26px;
  padding: 0;
  border-radius: 8px;
  font-size: 16px;
  line-height: 1;
}
.live2d-size-minus { grid-area: minus; }
.live2d-size-plus { grid-area: plus; }
.live2d-size-slider {
  grid-area: slider;
  width: 86px;
  accent-color: var(--accent-color);
  cursor: pointer;
}
.live2d-size-value {
  grid-area: value;
  justify-self: center;
  min-width: 48px;
  padding: 3px 7px;
  border-radius: 999px;
  font-size: 11px;
}
.live2d-size-step:disabled {
  cursor: not-allowed;
  opacity: .4;
}
.live2d-size-step:hover:not(:disabled),
.live2d-size-value:hover { color: var(--accent-color); }
.live2d-size-menu > summary:focus-visible,
.live2d-size-popover button:focus-visible,
.live2d-size-slider:focus-visible {
  outline: 2px solid var(--sakura-pink);
  outline-offset: 2px;
}
.live2d-close:hover,
.live2d-restore:hover,
.live2d-size-menu > summary:hover { color: var(--accent-color); border-color: var(--sakura-pink); }
/* ★ 2026-09-22：窄屏不再整体隐藏控件 —— 否则「先宽后窄」时看板娘仍在，
   关闭按钮却消失了，用户无法关闭。只收起大小菜单，保留关闭按钮。 */
@media (max-width: 900px) {
  .live2d-size-menu { display: none; }
}
</style>

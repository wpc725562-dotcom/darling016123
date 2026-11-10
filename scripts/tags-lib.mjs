// 标签 frontmatter 的读写工具（normalize-tags / check-tags / gen-tags 共用）
//
// ⚠️ 两个已踩过的坑，这里一次性处理掉：
//   1. `^tags:\s*` 的 `\s` 会吃掉换行 ⇒ 块式写法被误解析成「值 = '- xxx'」。
//      这里用 `[ \t]*` 限定为水平空白。
//   2. 文件可能有 BOM，`^\uFEFF?---` 才匹配得到 frontmatter（否则整段被当正文忽略）。

const BOM = '\uFEFF'

export function splitFrontmatter(text) {
  const hasBom = text.startsWith(BOM)
  const body = hasBom ? text.slice(1) : text
  const m = body.match(/^---\r?\n([\s\S]*?)\r?\n---(\r?\n|$)/)
  if (!m) return null
  // ⚠️ 行尾必须从**分隔符本身**判断，不能用 `body.includes('\r\n')`。
  //    本库存在**混合行尾**文件：frontmatter 用 LF、正文用 CRLF（如
  //    `posts/computer/notes/pengge-C-指针-二维数组传参.md`）。
  //    用全文件判断会得出 `\r\n`（2 字符），于是 fmStart 多算 1 个字符 ⇒
  //    head 变成 `---\nt`，正文首字母被吞进 frontmatter。
  const nl = m[0].charAt(3) === '\r' ? '\r\n' : '\n'
  // ⚠️ 必须用**算术**求出 head / tail 的切点。
  //    早先版本用 `body.slice(sp.fm.length)` 重建，少了开头的 `---\n` 4 个字符 ⇒
  //    写出来会「丢掉开头的 ---、并把 fm 最后 4 个字符顶到正文里」。
  //    实测后果：`tags:\n  - 日语` + `outline: deep` ⇒ `- 日语deep`，且文件不再有 frontmatter。
  const fmStart = m.index + 3 + nl.length
  const fmEnd = fmStart + m[1].length
  const head = body.slice(0, fmStart)
  if (!head.endsWith('---' + nl)) throw new Error('splitFrontmatter：head 边界算错（行尾判断有误）')
  // ⚠️ 收尾的 `---` 必须**留在 tail 里**（它是分隔符，不能吞掉）。
  //    早先版本写成 `fmEnd + nl.length + 3`，等于把收尾 `---` 吃掉 ⇒
  //    重建出的文件只有一个 `---`，frontmatter 直接失效。
  return {
    hasBom,
    fm: m[1],
    nl,
    head,
    tail: body.slice(fmEnd),
  }
}

/** 重建整份文件：head + 新 frontmatter + tail */
export function rebuild(sp, newFm) {
  return (sp.hasBom ? BOM : '') + sp.head + newFm + sp.tail
}

/** 从 frontmatter 文本里读出 tags 数组（保持原顺序、已去重前的原样） */
export function readTags(fm) {
  const mt = fm.match(/^tags:[ \t]*(.*)$/m)
  if (!mt) return null
  const inline = mt[1].trim()
  const out = []
  if (inline) {
    if (inline.startsWith('[')) {
      for (const x of inline.replace(/^\[|\]$/g, '').split(',')) out.push(x.trim().replace(/^["']|["']$/g, ''))
    } else {
      out.push(inline.replace(/^["']|["']$/g, ''))
    }
  } else {
    const after = fm.slice(mt.index + mt[0].length)
    for (const line of after.split('\n')) {
      if (/^[ \t]*-[ \t]*\S/.test(line)) out.push(line.replace(/^[ \t]*-[ \t]*/, '').trim().replace(/^["']|["']$/g, ''))
      else if (line.trim() === '') continue
      else break
    }
  }
  return out.filter(Boolean)
}

/** 把 frontmatter 里的 tags 块整体替换成 newTags（块式写法）。返回新的 frontmatter 文本 */
export function setTags(fm, newTags, nl = '\n') {
  // 新增的行必须沿用文件自己的行尾（本库多数 LF，但 guide/ 下有若干 CRLF 文件）
  const block = ['tags:', ...newTags.map((t) => '  - ' + t)].join('\n').replace(/\n/g, nl)
  const mt = fm.match(/^tags:[ \t]*(.*)$/m)
  if (!mt) {
    // 没有 tags ⇒ 插到 frontmatter 末尾
    return fm.replace(/\s*$/, '') + nl + block
  }
  // 求出 tags 块的范围（tags 行 + 紧随其后的 `- ` 行）
  // ⚠️ 用 `/^tags:/`，不能用 `/^tags:[ \t]/` —— 块式写法的冒号后**直接换行**，没有空格。
  const lines = fm.split('\n')
  let start = -1
  for (let i = 0; i < lines.length; i++) if (/^tags:/.test(lines[i])) { start = i; break }
  if (start < 0) return fm.replace(/\s*$/, '') + nl + block
  let end = start
  if (lines[start].replace(/^tags:[ \t]*/, '').trim() === '') {
    let i = start + 1
    while (i < lines.length && /^[ \t]*-[ \t]*\S/.test(lines[i])) i++
    end = i - 1
  }
  return [...lines.slice(0, start), ...block.split('\n'), ...lines.slice(end + 1)].join('\n')
}

export function sameTags(a, b) {
  return a.length === b.length && a.every((x, i) => x === b[i])
}

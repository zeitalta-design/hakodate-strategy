# HAKODATE TOURISM STRATEGY

函館観光の都市戦略提案サイト。
函館市観光動向調査を基に、「通過都市」から「滞在都市」への転換戦略を提案する。

---

## サイト構造

```
hakodate_tourism_strategy/
├─ index.html                 ← トップページ（市長向け30秒サマリー）
├─ analysis/index.html        ← 構造分析（データ分析レポート）
├─ strategy/index.html        ← 全体戦略（戦略フレームワーク）
├─ night-economy/index.html   ← Night Economy（施策ページ）
├─ goryokaku-2/index.html     ← Goryokaku 2.0（施策ページ）
├─ jomon/index.html           ← Jomon Experience（施策ページ）
├─ experience-liner/index.html← Experience Liner（施策ページ）
├─ summer-capital/index.html  ← Summer Capital（施策ページ）
├─ impact/index.html          ← 経済効果
├─ roadmap/index.html         ← 実行ロードマップ
├─ proposal/index.html        ← 提案概要・About
├─ assets/
│  ├─ css/
│  │  ├─ reset.css            ← リセットCSS
│  │  ├─ style.css            ← メインスタイル（デザインシステム）
│  │  └─ components.css       ← ページ固有コンポーネント
│  ├─ js/
│  │  └─ main.js              ← ナビ・スクロール・アニメーション
│  ├─ img/
│  │  ├─ hero/                ← Hero画像（現在不使用）
│  │  ├─ charts/              ← チャート画像（HTML/CSSで代替中）
│  │  ├─ projects/            ← プロジェクト画像
│  │  └─ icons/               ← アイコン
│  └─ pdf/
│     ├─ summary.pdf          ← 要約PDF（差し替え用）
│     ├─ strategy.pdf         ← 戦略PDF（差し替え用）
│     └─ impact.pdf           ← 経済効果PDF（差し替え用）
└─ README.md
```

---

## 編集ガイド

### テキスト差し替え

各HTMLファイル内の `<!-- TODO: ... -->` コメントが差し替え箇所を示す。
主な差し替え対象：

| 場所 | 内容 |
|------|------|
| `index.html` KPIカード | 観光入込客数、宿泊数、消費額の正確な値 |
| `index.html` バーチャート | 滞在日数・訪問先の割合（観光動向調査準拠） |
| `analysis/index.html` 全体 | 各DATA項目の数値・比率 |
| `impact/index.html` | 経済効果の試算値 |
| `summer-capital/index.html` | 気温データ |
| `proposal/index.html` | 提案者プロフィール |

### 画像差し替え

| ディレクトリ | 用途 |
|-------------|------|
| `assets/img/projects/` | 各施策の参考画像 |
| `assets/img/hero/` | Hero画像（必要な場合） |
| `assets/img/charts/` | データ可視化画像（必要な場合） |

画像は現在プレースホルダー（CSS背景色ブロック）で表示。
`<img>` タグまたは背景画像として差し替え可能。

### PDF差し替え

`assets/pdf/` 内のPDFファイルを差し替えるだけで、
提案概要ページのダウンロードリンクが更新される。

---

## 色・フォントの調整

`assets/css/style.css` の `:root` セクションで管理。

```css
:root {
  --navy-800: #1a2a3a;    /* メインカラー */
  --navy-600: #2d4a6f;    /* アクセントネイビー */
  --gray-50:  #f8f9fb;    /* セクション背景 */
  --accent:   #c49a3c;    /* アクセント金（未使用・予備） */
  --font: 'Noto Sans JP'; /* 日本語フォント */
  --font-en: 'Inter';     /* 英字フォント */
  --content-width: 800px; /* 本文幅 */
  --wide-width: 1080px;   /* ワイド幅 */
  --section-gap: 100px;   /* セクション間隔 */
}
```

---

## ページ追加方法

1. 新しいディレクトリを作成（例: `new-page/`）
2. `index.html` を既存ページからコピー
3. ヘッダーナビ、フッターリンクに追加
4. `page-hero` セクションのタイトル・説明を変更
5. セクションを `section` / `section--gray` / `section--navy` で交互に配置

---

## 技術仕様

- **フレームワーク不使用** — 純粋なHTML/CSS/JS
- **外部依存** — Google Fonts（Noto Sans JP, Inter）のみ
- **レスポンシブ** — 768px / 1024px ブレークポイント
- **アニメーション** — IntersectionObserver によるスクロール表示のみ
- **印刷対応** — 各ページ印刷可能

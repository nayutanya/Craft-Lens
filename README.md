# Craft Lens
ハンドメイド作品の出品支援ツールです。

## 開発背景
私自身がハンドメイド作品を出品する際に、作品の魅力を言語化する難しさと出品作業にかかる心理的ハードルを痛感してきました。SNS上でも「制作は楽しいが、事務的な出品作業が苦手」という声を多く目にしました。
「作家がもっと創作活動に集中できる環境を作りたい」という想いから、出品作業の負担を取り除くツールとしてCraft Lensを開発しました。

## デモ
**ホーム画面**
<img width="1040" height="739" alt="craftlens1" src="https://github.com/user-attachments/assets/2eef3e88-cf32-4e4c-a69e-ff242d148d19" />

**AI解析中（ローディング）**
<img width="1040" height="734" alt="craftlens2" src="https://github.com/user-attachments/assets/652ef9a3-c2f1-4307-ad84-c8cd0f8e0314" />

**ギャラリー一覧**
<img width="1030" height="742" alt="craftlens3" src="https://github.com/user-attachments/assets/39d5ec3c-f8e5-4a5b-87cd-acabc2307f58" />

**作品詳細**
<img width="1029" height="728" alt="craftlens4" src="https://github.com/user-attachments/assets/430e9bc4-7749-40f9-acb7-8d7f7948e7c2" />

## URL
https://craft-lens.onrender.com  
※無料サーバーを利用しているため、初回アクセス時に起動まで30秒〜1分ほどかかる場合があります。

## 機能
- **AI画像解析**:アップロードされた作品画像から、タイトルと説明文を自動生成。
- **ハイブリッド価格査定**:
  - 材料費と制作時間に基づく「原価計算」
  - AIによる「市場相場推測」
  - 上記を組み合わせた柔軟な査定ロジックを搭載。
- **作品管理ギャラリー**: 保存された作品を一覧表示し、詳細情報をいつでも確認可能。

## 使用技術
- **Backend** : Python 3.10+, FastAPI
- **Frontend** : JavaScript (Vanilla JS), HTML5, CSS3, Bootstrap 5
- **Database** : PostgreSQL
- **AI API** : OpenAI API (GPT-4o-mini / Vision)
- **Infrastructure** : Docker / Docker Compose, Render (Deployment)

## 工夫した点

### 【技術・ロジック面】
**ハイブリッド査定ロジック**  
ユーザーが材料費や制作時間を入力しなかった場合でも、AIが画像から素材の質感や手間の多さを推測し、市場相場に照らし合わせた適切な価格を提示します。

**防衛的プログラミング**  
外部API（OpenAI）の回答が不安定な場合でも、Python側で例外処理と最低保証価格の設定を行い、システムが停止したり「0円」と表示されたりしない設計を徹底しました。

**コストとリスクの管理**  
API利用料の急増を防ぐため、OpenAI側での予算制限（Usage Limit）を設定し、実運用を見据えたリスク管理を行っています。

### 【UX・フロントエンド面】
**ローディング設計**  
AIの解析待ち時間（5〜10秒）に対し、JavaScriptで動的なローディング画面を制御。進捗を視覚化することでユーザーの離脱を防いでいます。

**UI設計**  
制作時間を「1時間30分」と分割入力させる、価格をプロ風に四捨五入して表示するなど、作家の直感に寄り添った細部の設計を行いました。また生成テキストのワンクリックコピー機能や二重送信防止のボタン制御も実装しています。

## 今後の展開
- 複数画像アップロードによる査定精度の向上
- カテゴリー別の検索・フィルタリング機能
- 過去の出品データをもとにした売れやすい作品傾向の分析機能
- 材料の在庫・費用を管理するストック管理機能

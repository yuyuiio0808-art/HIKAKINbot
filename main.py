
import {
  Client,
  GatewayIntentBits,
  Events,
  type Message,
} from "discord.js";
import { logger } from "./lib/logger";

const ARIGATOU_PATTERNS = [
  "ありがとう",
  "ありがとございます",
  "ありがとうございます",
  "ありがとね",
  "ありがとな",
  "thx",
  "thanks",
  "thank you",
  "サンクス",
];

export function startBot(): void {
  const token = process.env["DISCORD_TOKEN"];
  if (!token) {
    logger.warn("DISCORD_TOKEN is not set. Discord bot will not start.");
    return;
  }

  const client = new Client({
    intents: [
      GatewayIntentBits.Guilds,
      GatewayIntentBits.GuildMessages,
      GatewayIntentBits.MessageContent,
    ],
  });

  client.once(Events.ClientReady, (readyClient) => {
    logger.info({ tag: readyClient.user.tag }, "Discord bot is ready!");
  });

  client.on(Events.MessageCreate, async (message: Message) => {
    if (message.author.bot) return;

    const content = message.content.toLowerCase();

    const arigatouMatched = ARIGATOU_PATTERNS.some((pattern) =>
      content.includes(pattern.toLowerCase()),
    );

    const nigaMatched =
      content.includes("ニガ") || content.includes("にが");

    const gameMatched =
      content.includes("ゲームしよう") ||
      content.includes("げーむしよう") ||
      content.includes("ゲームしましょう") ||
      content.includes("ゲームしない");

    const hikakinMatched =
      content.includes("hikakin") || content.includes("ひかきん");

    const mejiconMatched =
      content.includes("メジコン") || content.includes("めじこん");

    const restaMinMatched =
      content.includes("レスタミン") || content.includes("れすたみん");

    const lettuceMatched =
      content.includes("レタス") || content.includes("れたす");

    const seafoodMatched =
      content.includes("魚介") || content.includes("ぎょかい");

    const seikinMatched =
      content.includes("seikIn") || content.includes("せいきん");

    if (arigatouMatched) {
      await message.reply("ブンブン！当たり前のことをしただけですよ〜 😊");
    } else if (nigaMatched) {
      await message.reply("ニガ？僕は普通の肌の色しか知りません");
    } else if (gameMatched) {
      await message.reply("クカッ！HIKAKINゲームズで動画をとりませんか？");
    } else if (seikinMatched) {
      await message.reply("長らく会ってないですね");
    } else if (hikakinMatched) {
      await message.reply("どうも！HIKAKINです！");
    } else if (mejiconMatched) {
      await message.reply("次の企画はそれにしよう！");
    } else if (restaMinMatched) {
      await message.reply("SEIKINが好きです！");
    } else if (lettuceMatched) {
      await message.reply("いきなり野菜の話ですか？");
    } else if (seafoodMatched) {
      await message.reply(
        "マスクで汚染花粉からの被害を回避できます。また、魚介類は産地がわからないものは食べません。日本産の魚介類は終わってます。特に大型魚類と貝類は放射性物質が濃縮されますんでお気をつけて。",
      );
    }
  });

  client.login(token).catch((err) => {
    logger.error({ err }, "Failed to login to Discord");
  });
}

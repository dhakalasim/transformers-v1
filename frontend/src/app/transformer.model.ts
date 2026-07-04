export interface BotInfo {
  name: string;
  conversions: string[][];
}

export interface TransformRequest {
  content: string;
  from_format: string;
  to_format: string;
}

export interface TransformResponse {
  bot_name: string;
  result: string;
}

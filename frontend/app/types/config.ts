export interface AppConfig {
  modelProvider: string;
  dataDir: string;
  toolSet: string;
  mcpServer: string;
}

export interface ModelConfig {
  embedModel: string;
  chatModel: string;
}

export interface ChatConfig {
  starterQuestions: string[];
}

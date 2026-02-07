export const TextDeltaPartType = "text-delta";

export type TextDeltaPart = {
    id: string;
    type: typeof TextDeltaPartType;
    delta: string;
}

import { HubConnection } from "@microsoft/signalr";
import { RefObject } from "react";

export enum ChatRoles {
    User,
    Assistant
}

interface TChatMessage {
    id: string;
    content: string;
    role: string;
}

interface TAddChatMessageDto {
    chatId: string,
    content: string,
    role: string
}

interface TStreamMessage {
    chatId: string,
    content: string,
    role: string
}

interface TLoginUserDto {
    firstName: string,
    lastName: string
}

interface TChatMessageDto {
    id: string,
    content: string,
    role: string,
    chatId: string
}

interface TUser {
    id: string,
    name: string
}

interface TUserDto {
    id: string,
    firstName: string,
    lastName: string
}

interface TCreateChatDto {
    userId: string
}

interface TChatDto {
    id: string,
    title: string,
    userId: string
}

interface TAuthContext {
    user: TUserDto | null;
    loginAction: (data: TLoginUserDto) => Promise<void>;
    logOutAction: () => void;
}

interface TAppContext {
    showSlide: boolean;
    setShowSlide: (value: boolean) => void;
    Mobile: boolean;
    setMobile: (value: boolean) => void;
  }

interface TChatContext {
    chats: TChatDto[]; // Replace with a specific type if known
    setChats: React.Dispatch<React.SetStateAction<TChatDto[]>>; // Replace with a specific type if known
    messages: TChatMessage[];
    setMessages: React.Dispatch<React.SetStateAction<TChatMessage[]>>;
    loading: boolean;
    setLoading: React.Dispatch<React.SetStateAction<boolean>>;
    msgEnd: RefObject<HTMLDivElement>;
    joinChat: (userId: string, chatId: string) => Promise<void>;
    activeChatId: string | null;
    setActiveChatId: React.Dispatch<React.SetStateAction<string | null>>;
    chatResponseLoading: boolean;
    partialMessage: string;
    setPartialMessage: React.Dispatch<React.SetStateAction<string>>;
    setChatResponseLoading: React.Dispatch<React.SetStateAction<boolean>>;
    firstChunkReceived: boolean;
    setFirstChunkRecieved: React.Dispatch<React.SetStateAction<boolean>>;
    connectionRef: React.MutableRefObject<HubConnection | null>;
    getAssistantResponse: (userId: string, message: string) => Promise<void>;
}

export type {
    TChatMessage,
    TAddChatMessageDto,
    TCreateChatDto,
    TLoginUserDto,
    TChatMessageDto,
    TChatContext,
    TAuthContext,
    TAppContext,
    TUserDto,
    TChatDto,
    TStreamMessage,
    TUser
};

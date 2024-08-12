const BASEURL : string = "/api";

const ENDPOINTS = {
    LOGIN_USER : `${BASEURL}/users/login`,
    CHATS_BY_USER : (userId : string) => `${BASEURL}/chat/${userId}`,
    CHAT_CONVERSATIONS: (chatId : string) => `${BASEURL}/chat-histories/${chatId}`,
    CREATE_CHAT: `${BASEURL}/chat/create`,
    DELETE_CHAT: (chatId: string) => `${BASEURL}/chat/${chatId}`,
    HUB_CONNECTION: "http://localhost:5031/chatHub"
}

export default ENDPOINTS;
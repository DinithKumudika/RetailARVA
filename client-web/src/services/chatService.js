import axios from "axios";

export const getChatsByUser = async (user) => {
    try {
        const response = await axios.get(`/api/chat/${user.id}`);
        const chats = response.data.data;
        return chats;
    } catch (error) {
        throw error;
    }
};

export const getChatConversation = async (chatId) => {
    try {
        const response = await axios.get(`/api/chat-histories/${chatId}`);
        const chatHistory = response.data.data;
        return chatHistory;
    } catch (error) {
        throw error;
    }
}

export const addChatMessage = async (chatId, message) => {
    const newMessage = {
        "chatId": chatId,
        "content": message,
        "role": "User"
    }
    try {
        const response = await axios.post(`/api/chat-histories/${chatId}`, newMessage, {
            headers: {
                "Content-Type": "application/json",
            },
        });

        const message = response.data.data;
        console.log(message);
        return message;
    } catch (error) {
        throw error;
    }
}

export const craeteNewChat = async (userId) => {
    try {
        const createChat = {
            "userId": userId
        };

        const response = await axios.post("/api/chat/create", createChat, {
            headers: {
                "Content-Type": "application/json",
            },
        });

        const newMessage = response.data.data;
        console.log(newMessage);
        return newMessage;
    } catch (error) {
        throw error;
    }
}

export const deleteChatById = async (chatId) => {
    try {
        const response = await axios.delete(`/api/chat/${chatId}`);
        if (response.status === 204) {
            return true;
        }
        return false;
    } catch (error) {
        throw error;
    }
}
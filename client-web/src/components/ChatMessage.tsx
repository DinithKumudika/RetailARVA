import { ChatRoles } from "../utils/types";

interface ChatMessageProps {
    message: {
        id: string;
        content: string;
        role: string;
    };
}

const ChatMessage : React.FC<ChatMessageProps> = ({ message }) => {
    return (
        <div
            className={`w-full flex ${message.role === ChatRoles[ChatRoles.Assistant] ? "justify-start" : "justify-end"} my-2`}
        >
            <span
                className={`flex rounded-md max-w-[75%] ${message.role === ChatRoles[ChatRoles.Assistant] ? "justify-start" : "justify-end"} items-start gap-2 lg:gap-5 my-2 p-3 ${message.role === ChatRoles[ChatRoles.Assistant] ? "bg-gray-800/80" : "bg-gray-600/80"}`}
            >
                {message.role === ChatRoles[ChatRoles.Assistant] && (
                    <img
                        src="/icon.png"
                        alt="assistant"
                        className="w-10 h-10 rounded object-cover"
                    />
                )}
                <p className="text-white text-[15px]">{message.content}</p>
            </span>
        </div>
    )
}

export default ChatMessage
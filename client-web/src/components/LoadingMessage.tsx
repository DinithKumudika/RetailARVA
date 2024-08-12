import { ChatRoles } from "../utils/types";

interface LoadingMessageProps {
    role: string;
};


const LoadingMessage : React.FC<LoadingMessageProps> = ({ role }) => {
    return (

        <div
            className={`w-full flex ${role === ChatRoles[ChatRoles.Assistant] ? "justify-start" : "justify-end"} my-2`}
        >
            <span
                className={`flex rounded-md max-w-[75%] ${role === ChatRoles[ChatRoles.Assistant] ? "justify-start" : "justify-end"} items-start gap-2 lg:gap-5 my-2 p-3 ${role === ChatRoles[ChatRoles.Assistant] ? "bg-gray-800/80" : "bg-gray-600/80"}`}
            >
                <div className="flex items-center space-x-2">
                    <div className="h-8 w-8 bg-zinc-300 rounded-full animate-pulse"></div>
                    <div className="h-4 w-16 bg-zinc-300 rounded-full animate-pulse"></div>
                </div>
            </span>
        </div>
    )
}

export default LoadingMessage
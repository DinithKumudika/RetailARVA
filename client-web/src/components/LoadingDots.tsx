interface LoadingDotsProps {
    size: number;
};

const LoadingDots : React.FC<LoadingDotsProps> = ({ size }) => {
    return (
        <div className='flex space-x-2 justify-center items-center bg-grey h-screen'>
            <div className={`h-${size} w-${size} bg-white rounded-full animate-bounce [animation-delay:-0.3s]`}></div>
            <div className={`h-${size} w-${size} bg-white rounded-full animate-bounce [animation-delay:-0.15s]`}></div>
            <div className={`h-${size} w-${size} bg-white rounded-full animate-bounce`}></div>
        </div>
    )
}

export default LoadingDots
export default function ErrorBanner({ message }) {
  if (!message) return null;

  return (
    <div className="error-banner bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium">
      {message}
    </div>
  );
}

interface QrCodeDisplayProps {
  qrImageUrl: string;
  secret: string;
}

export function QrCodeDisplay({ qrImageUrl, secret }: QrCodeDisplayProps) {
  return (
    <div className="flex flex-col items-center gap-4">
      <img
        src={qrImageUrl}
        alt="MFA QR Code"
        className="w-48 h-48 border rounded shadow"
      />

      <div className="text-sm text-gray-600">
        Secret: <span className="font-mono">{secret}</span>
      </div>
    </div>
  );
}

import "./globals.css";

export const metadata = {
  title: "Cosmic Explorer",
  description: "Discover the archetypal themes that may shape your upcoming psychedelic journey",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

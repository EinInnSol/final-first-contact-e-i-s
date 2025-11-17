export const metadata = {
  title: 'First Contact E.I.S. - Caseworker Dashboard',
  description: 'AI-Powered Early Intervention System',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

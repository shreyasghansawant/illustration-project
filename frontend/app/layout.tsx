import './globals.css'

export const metadata = {
  title: 'Illustration Personalizer',
  description: 'Personalize illustrations with your photos',
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


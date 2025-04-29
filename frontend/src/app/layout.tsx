import './globals.css'
import { Inter } from 'next/font/google'
import type { Metadata } from 'next'
import Link from 'next/link'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'My Store – Hobby Hosting',
  description: 'Check out this slick storefront built with Next.js + FastAPI!',
  openGraph: {
    title: 'My Store – Hobby Hosting',
    description: 'Simple, clean, fast. See the live product catalog.',
    url: 'https://hobbyhosting.org',
    siteName: 'Hobby Hosting',
    images: [
      {
        url: 'https://hobbyhosting.org/og-image.jpg',
        width: 1200,
        height: 630,
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'My Store – Hobby Hosting',
    description: 'Simple, clean, fast. See the live product catalog.',
    images: ['https://hobbyhosting.org/og-image.jpg'],
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <nav className="p-4 flex gap-4 bg-gray-100">
          <Link href="/" className="font-semibold">Home</Link>
          <Link href="/products" className="font-semibold">Products</Link>
        </nav>
        {children}
      </body>
    </html>
  )
}

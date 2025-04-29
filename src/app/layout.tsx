import './globals.css'
import { Inter } from 'next/font/google'
import type { Metadata } from 'next'
import Link from 'next/link'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'My Store',
  description: 'Next.js E-commerce starter',
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

// frontend/src/app/checkout/page.tsx

'use client'

import { loadStripe } from '@stripe/stripe-js'

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!)

export default function CheckoutPage() {
  const handleCheckout = async () => {
    const res = await fetch('http://localhost:8000/create-checkout-session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_name: 'T-shirt', price: 2000 })
    })

    const data = await res.json()
    const stripe = await stripePromise
    stripe?.redirectToCheckout({ sessionId: data.id })
  }

  return <button onClick={handleCheckout}>Köp för 200 kr</button>
}

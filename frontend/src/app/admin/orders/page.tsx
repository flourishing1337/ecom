'use client'

import useSWR from 'swr'

// Define types for the order and items
type OrderItem = {
  product_name: string
  quantity: number
  unit_price: number
}

type Order = {
  order_id: string
  status: string
  total_amount: number
  created_at: string
  items: OrderItem[]
}

const fetcher = (url: string) => fetch(url).then(res => res.json())

export default function OrdersPage() {
  const { data, error, isLoading } = useSWR<Order[]>('https://api.hobbyhosting.org/orders', fetcher)

  if (error) return <div>❌ Kunde inte ladda ordrar.</div>
  if (isLoading || !data) return <div>⏳ Laddar...</div>

  return (
    <div className="p-4 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Ordrar</h1>
      {data.length === 0 ? (
        <p className="text-gray-500">Inga ordrar hittades.</p>
      ) : (
        data.map((order) => (
          <div
            key={order.order_id}
            className="border border-gray-200 rounded-xl p-4 mb-4 shadow-sm"
          >
            <div className="text-lg font-semibold">
              Order #{order.order_id} – {order.status.toUpperCase()}
            </div>
            <div className="text-sm text-gray-600">
              Total: ${order.total_amount.toFixed(2)}
            </div>
            <div className="text-sm text-gray-500">
              Skapad: {new Date(order.created_at).toLocaleString()}
            </div>
            <ul className="mt-2 space-y-1">
              {order.items.map((item, i) => (
                <li key={i} className="text-sm">
                  • {item.quantity} × {item.product_name} (${item.unit_price.toFixed(2)} styck)
                </li>
              ))}
            </ul>
          </div>
        ))
      )}
    </div>
  )
}

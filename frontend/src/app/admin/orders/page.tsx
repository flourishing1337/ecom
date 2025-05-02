'use client'

import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(res => res.json())

export default function OrdersPage() {
  const { data, error } = useSWR('https://api.hobbyhosting.org/orders', fetcher)

  if (error) return <div>❌ Kunde inte ladda ordrar.</div>
  if (!data) return <div>⏳ Laddar...</div>

  return (
    <div className="p-4 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Ordrar</h1>
      {data.map((order: any) => (
        <div key={order.order_id} className="border border-gray-200 rounded-xl p-4 mb-4">
          <div className="text-lg font-semibold">
            Order #{order.order_id} – {order.status.toUpperCase()}
          </div>
          <div className="text-sm text-gray-600">Total: ${order.total_amount.toFixed(2)}</div>
          <div className="text-sm text-gray-500">Skapad: {new Date(order.created_at).toLocaleString()}</div>
          <ul className="mt-2 space-y-1">
            {order.items.map((item: any, i: number) => (
              <li key={i} className="text-sm">
                • {item.quantity} x {item.product_name} (${item.unit_price.toFixed(2)} styck)
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  )
}

'use client'

import useSWR from 'swr'

type Product = {
  id: number
  name: string
  price: number
}

const fetcher = (url: string) => fetch(url).then((res) => res.json())

export default function Products() {
  const { data: products, error } = useSWR<Product[]>('http://127.0.0.1:8000/products', fetcher)

  if (error) return <div>Failed to load</div>
  if (!products) return <div>Loading...</div>

  return (
    <main className="p-8">
      <h1 className="text-3xl font-bold mb-6">Our Products</h1>
      <div className="grid grid-cols-2 gap-4">
        {products.map((p) => (
          <div key={p.id} className="border p-4 rounded shadow">
            <h2 className="text-xl font-semibold">{p.name}</h2>
            <p className="text-gray-600">${p.price}</p>
          </div>
        ))}
      </div>
    </main>
  )
}

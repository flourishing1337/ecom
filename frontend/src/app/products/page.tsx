'use client'

import useSWR from 'swr'

type Product = {
  id: number
  name: string
  price: number
}

const fetcher = (url: string) => fetch(url).then((res) => res.json())

export default function Home() {
  return (
    <main className="p-6 flex flex-col items-center justify-center text-center space-y-6 max-w-xl mx-auto">
      <h1 className="text-3xl sm:text-4xl font-bold">Välkommen, snart dyker vi...</h1>
      
      <div className="w-full aspect-video max-w-md sm:max-w-lg md:max-w-xl rounded overflow-hidden shadow-lg">
        <video
          controls
          className="w-full h-full object-cover"
          poster="/video-poster.jpg" // optional placeholder image
        >
          <source src="/demo.mp4" type="video/mp4" />
          Din webbläsare stödjer inte video-taggen.
        </video>
      </div>
    </main>
  )
}

import { NextRequest, NextResponse } from "next/server";
import { mockResponse } from "@/lib/mock-data";

export async function POST(req: NextRequest) {
  const { query } = await req.json();

  try {
    const response = await fetch("http://localhost:8000/learn/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ user_input: query }),
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();

    // const data = mockResponse;

    return NextResponse.json(data);
  } catch (error) {
    console.error("Error during search:", error);
    return NextResponse.json(
      { error: "Failed to fetch data from backend" },
      { status: 500 }
    );
  }
}

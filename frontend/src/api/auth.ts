const API_URL = import.meta.env.VITE_API_URL

export async function login(username: string, password: string): Promise<void> {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        body: new URLSearchParams({username, password}),
        credentials: "include"
    });

    if (!response.ok) {
        throw new Error("Identifiants invalides");
    }
}

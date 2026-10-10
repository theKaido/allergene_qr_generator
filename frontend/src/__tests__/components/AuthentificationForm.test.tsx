import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, it, expect, vi} from "vitest"
import AuthentificationForm from "../../components/AuthentificationForm"
import { login } from "../../api/auth"

vi.mock("../../api/auth")

describe("AuthentificationForm", () => {
    it("affiche le mot de passe en clair au clic sur l'oeil", async () => {
        render(<AuthentificationForm />)

        const champMotDePasse = screen.getByPlaceholderText("************")
        expect(champMotDePasse).toHaveAttribute("type", "password")

        const boutonOeil = screen.getByRole("button", { name: "Afficher le mot de passe"})
        await userEvent.click(boutonOeil)

        expect(champMotDePasse).toHaveAttribute("type", "text")
    })

    it("affiche un message d'erreur si la connexion échoue", async () => {
        vi.mocked(login).mockRejectedValue(new Error())
        render(<AuthentificationForm/>)

        await userEvent.type(screen.getByLabelText("Identifiant"), "test")
        await userEvent.type(screen.getByLabelText("Mot de Passe"), "mauvais")
        await userEvent.click(screen.getByRole("button", {name: "Se connecter"}))

        expect(await screen.findByRole("alert")).toHaveTextContent("Identifiant ou mot de passe incorrect")
    })

    it("affiche aucun message d'erreur si la conenxion reussi", async () => {
        vi.mocked(login).mockResolvedValue(undefined)
        render(<AuthentificationForm/>)

        await userEvent.type(screen.getByLabelText("Identifiant"), "test")
        await userEvent.type(screen.getByLabelText("Mot de Passe"), "secret")
        await userEvent.click(screen.getByRole("button", {name: "Se connecter"}))

        expect(login).toHaveBeenCalledWith("test","secret")
        expect(screen.queryByRole("alert")).toBeNull()
    })
})
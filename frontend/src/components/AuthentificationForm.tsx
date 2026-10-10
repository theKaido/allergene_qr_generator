import { PiForkKnife } from "react-icons/pi";
import { FcGoogle } from "react-icons/fc";
import { FiLock } from "react-icons/fi";
import { CiUser } from "react-icons/ci";
import { IoMdEye, IoMdEyeOff } from "react-icons/io";
import {useState, type SubmitEvent} from "react";
import {login} from "../api/auth"

function AuthentificationForm() {
    const [showPassword, setShowPassword] = useState(false)
    const [error, setError] = useState<string | null>(null)

    async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
        event.preventDefault();
        const formData = new FormData(event.currentTarget);
        const username = String(formData.get("username") ?? "");
        const password = String(formData.get("password") ?? "");
        setError(null);
        try {
            await login(username, password);
            console.log("connecté")
        } catch {
            setError("Identifiant ou mot de passe incorrect");
        }
    }

    return (
         <div className="d-flex flex-column align-items-center login-form">
            <h2 className="fw-bold"><PiForkKnife className="main-icon"/> Kaleidogram</h2>
            <p className="mt-2">Identifiez les allergènes en un coup d'oeil</p>
            <button
                type="button"
                className="btn btn-light d-flex align-items-center justify-content-center gap-2 mt-3 w-100"
            >
                    <FcGoogle/>Se connecter avec Google
            </button>
            <div className="d-flex align-items-center w-100 my-5">
                <hr className="flex-grow-1" />
                <b className="mx-2">OU PAR IDENTIFIANT</b>
                <hr className="flex-grow-1" />
            </div>
            <form onSubmit={handleSubmit} className="d-flex flex-column align-items-center w-100">
                <label htmlFor="main-username" className="align-self-start mb-1">Identifiant</label>
                <div className="input-group mb-3">
                    <span className="input-group-text" id="username-addon">
                        <CiUser size={20} />
                    </span>
                    <input
                        id="main-username"
                        type="text"
                        className="form-control"
                        placeholder="identifiant"
                        name="username"
                    />
                </div>
                <label htmlFor="main-password" className="align-self-start mb-1">Mot de Passe</label>
                <div className="input-group mb-2">
                    <span className="input-group-text" id="password-addon">
                        <FiLock size={20} />
                    </span>
                    <input
                        id="main-password"
                        type={showPassword ? 'text' : 'password'}
                        className="form-control"
                        placeholder="************"
                        name="password"
                    />
                    <button
                        type="button"
                        className="input-group-text"
                        id="show-password"
                        aria-label={showPassword ? "Masquer le mot de passe" : "Afficher le mot de passe"}
                        onClick={() => setShowPassword(!showPassword)}
                    >
                        {showPassword ? <IoMdEyeOff size={20}/> : <IoMdEye size={20} /> }
                    </button>
                </div>
                <div className="d-flex justify-content-between w-100 mt-2">
                    <div className="d-flex align-items-center justify-content-center gap-1">
                        <input
                            type="checkbox"
                            id="remember-user"
                            name="bouton-se-souvenir"
                        />
                        <label htmlFor="remember-user">Se souvenir de moi</label>
                    </div>
                    <div>
                        <a
                            href="https:motdepasseoublie.com/aremplaceraveclevrailien"
                            className="lien-action text-decoration-none fw-bold"
                        >
                            Mot de passe oublié
                        </a>
                    </div>
                </div>
                <div className="w-100">
                    <button type="submit" className="btn connexion w-100 mt-4 mb-2">Se connecter</button>
                </div>
                {error && <p className="text-danger mb-0" role="alert">{error}</p>}
            </form>
            <div className="d-flex flex-nowrap text-nowrap m-3 gap-1">
                <p className="mb-0">Nouveau sur Kaleidogram ?</p>
                <a
                    type="text"
                    className="text-decoration-none fw-bold lien-action"
                    href="https://github.com/theKaido/Kaleidogram">
                    Créer un compte
                </a>
            </div>
        </div>
    )
}

export default AuthentificationForm
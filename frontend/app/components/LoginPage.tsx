"use client";
import React, { useEffect } from "react";
import Link from "next/link";
import * as Yup from "yup";
import { Formik, Form, Field, ErrorMessage, FormikHelpers } from "formik";
import Hr from "./Hr";
import { apiClientUser } from "@/data/api";
import { TokensType } from "@/types/types";
import { useDispatch } from "react-redux";
import { login } from "@/data/auth_slise";
import { usePathname, useRouter } from "next/navigation";

const loginSchema = Yup.object().shape({
    email: Yup.string().email().required().trim().label("Email"),
    password: Yup.string().min(8).required().label("Password"),
});

const initialValues = {
    email: "",
    password: "",
};

type LoginType = typeof initialValues;

function LoginPage() {
    const dispatch = useDispatch();
    const router = useRouter();
    const pathname = usePathname();
    const [nextUrl, setNextUrl] = React.useState<string>("/");

    async function submitLogin(values: LoginType, formikHelpers: FormikHelpers<LoginType>) {
        await apiClientUser
            .post("/login/", values)
            .then((res) => {
                const data = res.data as TokensType;
                dispatch(login(data));
                router.replace(nextUrl);
            })
            .catch((err) => {
                const errorMsdg = err.response.data;
                for (const key in errorMsdg) {
                    formikHelpers.setFieldError(key, errorMsdg[key]);
                }
            });
    }

    useEffect(() => {
        if (pathname !== "/login") {
            setNextUrl(pathname);
        }
        router.replace("/login");
    }, []);

    return (
        <div className="flex flex-col justify-center h-screen items-center bg-slate-200">
            <div className="flex w-max-[1000px] w-[1000px]">
                <div className="w-1/2 flex items-center">
                    <div>
                        <h1 className="text-6xl font-bold text-blue-600">facebook-clone</h1>
                        <p className="text-2xl font-medium">
                            Facebook helps you connect and share with the people in your life.
                        </p>
                    </div>
                </div>
                <div className="w-1/2 flex items-center justify-end">
                    <div className="w-4/5 bg-white shadow-xl rounded-lg p-4">
                        <Formik initialValues={initialValues} onSubmit={submitLogin} validationSchema={loginSchema}>
                            <Form>
                                <div className="py-2">
                                    <Field
                                        type="email"
                                        name="email"
                                        className="w-full border p-4 text-xl rounded-md"
                                        placeholder="Email"
                                        autoComplete="email"
                                    />
                                    <ErrorMessage name="email" component="div" className="text-red-500 text-sm px-1" />
                                </div>
                                <div className="py-2">
                                    <Field
                                        type="password"
                                        name="password"
                                        className="w-full border p-4 text-xl rounded-md"
                                        placeholder="Password"
                                        autoComplete="current-password"
                                    />
                                    <ErrorMessage
                                        name="password"
                                        component="div"
                                        className="text-red-500 text-sm px-1"
                                    />
                                </div>
                                <button
                                    type="submit"
                                    className="w-full p-3 mt-4 bg-blue-600 text-xl font-medium rounded-md text-white"
                                >
                                    Log in
                                </button>
                                <div className="w-full flex flex-col items-center">
                                    <Hr color="bg-black" my={8} />
                                    <Link
                                        href={"/register"}
                                        className="bg-green-500 mt-2 text-center w-fit font-medium text-white px-8 py-2 rounded-md"
                                    >
                                        Create new account
                                    </Link>
                                </div>
                            </Form>
                        </Formik>
                    </div>
                </div>
            </div>
            <div className="h-56" />
        </div>
    );
}

export default LoginPage;

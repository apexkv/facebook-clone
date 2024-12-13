"use client";
import React from "react";
import Link from "next/link";
import * as Yup from "yup";
import { Formik, Form, Field, ErrorMessage, FormikHelpers } from "formik";
import { apiClientUser } from "@/data/api";
import { TokensType } from "@/types/types";
import { useDispatch } from "react-redux";
import { login } from "@/data/auth_slise";
import Hr from "./Hr";
import { useRouter } from "next/navigation";

const loginSchema = Yup.object().shape({
    full_name: Yup.string().required().trim().label("Full Name"),
    email: Yup.string().email().required().trim().label("Email"),
    password: Yup.string().min(8).required().label("Password"),
    password_confirm: Yup.string()
        .oneOf([Yup.ref("password")], "Passwords must match")
        .required()
        .label("Password Confirm"),
});

const initialValues = {
    full_name: "",
    email: "",
    password: "",
    password_confirm: "",
};

type RegisterType = typeof initialValues;

function RegisterPage() {
    const dispatch = useDispatch();
    const router = useRouter();

    async function submitRegister(values: RegisterType, formikHelpers: FormikHelpers<RegisterType>) {
        await apiClientUser
            .post("/register/", values)
            .then((res) => {
                const data = res.data as TokensType;
                dispatch(login(data));
                router.replace("/");
            })
            .catch((err) => {
                const errorMsdg = err.response.data;
                for (const key in errorMsdg) {
                    formikHelpers.setFieldError(key, errorMsdg[key]);
                }
            });
    }

    return (
        <div className="flex flex-col justify-center h-screen items-center bg-slate-200">
            <div className="flex w-max-[1000px] w-[1000px]">
                <div className="w-1/2 flex items-center">
                    <div>
                        <h1 className="text-6xl font-bold text-blue-600">facebook-clone</h1>
                        <p className="text-2xl font-medium">
                            Facebook helps you connect and share with the people in your life.
                        </p>

                        <div className="h-56" />
                    </div>
                </div>
                <div className="w-1/2 flex items-center justify-end">
                    <div className="w-4/5 bg-white shadow-xl rounded-lg p-4">
                        <Formik initialValues={initialValues} onSubmit={submitRegister} validationSchema={loginSchema}>
                            <Form>
                                <div className="py-2">
                                    <Field
                                        type="text"
                                        name="full_name"
                                        className="w-full border p-4 text-xl rounded-md"
                                        placeholder="Full Name"
                                        autoComplete="name"
                                    />
                                    <ErrorMessage
                                        name="full_name"
                                        component="div"
                                        className="text-red-500 text-sm px-1"
                                    />
                                </div>
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
                                <div className="py-2">
                                    <Field
                                        type="password"
                                        name="password_confirm"
                                        className="w-full border p-4 text-xl rounded-md"
                                        placeholder="Password Confirm"
                                        autoComplete="current-password"
                                    />
                                    <ErrorMessage
                                        name="password_confirm"
                                        component="div"
                                        className="text-red-500 text-sm px-1"
                                    />
                                </div>
                                <button
                                    type="submit"
                                    className="w-full p-3 mt-4 bg-blue-600 text-xl font-medium rounded-md text-white"
                                >
                                    Sign up
                                </button>
                                <div className="w-full flex flex-col items-center">
                                    <Hr color="bg-black" my={8} />
                                    <Link
                                        href={"/login"}
                                        className="bg-green-500 mt-2 text-center w-fit font-medium text-white px-8 py-2 rounded-md"
                                    >
                                        Login
                                    </Link>
                                </div>
                            </Form>
                        </Formik>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default RegisterPage;

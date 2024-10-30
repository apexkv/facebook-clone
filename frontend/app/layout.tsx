import type { Metadata } from 'next';
import localFont from 'next/font/local';
import './globals.css';
import AuthProvider from './components/AuthProvider';

const geistSans = localFont({
	src: './fonts/GeistVF.woff',
	variable: '--font-geist-sans',
	weight: '100 900',
});
const geistMono = localFont({
	src: './fonts/GeistMonoVF.woff',
	variable: '--font-geist-mono',
	weight: '100 900',
});

export const metadata: Metadata = {
	title: 'Facebook Clone',
	description: 'Facebook clone project',
};

export default function RootLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	return (
		<html lang="en" suppressHydrationWarning={true} data-gr-ext-installed data-new-gr-c-s-check-loaded>
			<body className={`${geistSans.variable} ${geistMono.variable} antialiased bg-neutral-900 !tracking-wide`}>
				<AuthProvider>{children}</AuthProvider>
			</body>
		</html>
	);
}

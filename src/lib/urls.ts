function hasProtocol(path: string): boolean {
	return /^[a-z][a-z\d+.-]*:/i.test(path) || path.startsWith('//');
}

export function asRootRelativePath(path?: string): string | undefined {
	if (!path || path.startsWith('#') || hasProtocol(path) || path.startsWith('/')) {
		return path;
	}

	if (path.startsWith('?')) {
		return path;
	}

	return `/${path.replace(/^\/+/, '')}`;
}

function getBasePath(): string {
	const baseUrl = import.meta.env.BASE_URL;
	if (!baseUrl || baseUrl === '/') {
		return '';
	}

	return baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;
}

function splitSuffix(path: string): [string, string] {
	const match = path.match(/^([^?#]*)(.*)$/);
	return [match?.[1] ?? path, match?.[2] ?? ''];
}

function looksLikeFilePath(path: string): boolean {
	const [pathname] = splitSuffix(path);
	const lastSegment = pathname.split('/').pop() ?? '';
	return lastSegment.includes('.');
}

export function withBase(path?: string): string | undefined {
	if (!path) {
		return path;
	}

	if (path.startsWith('#') || hasProtocol(path)) {
		return path;
	}

	const basePath = getBasePath();
	if (!basePath) {
		return path;
	}

	if (path === '/') {
		return `${basePath}/`;
	}

	if (path === basePath || path.startsWith(`${basePath}/`)) {
		return path;
	}

	if (path.startsWith('/')) {
		return `${basePath}${path}`;
	}

	return path;
}

export function withBasePath(path?: string): string | undefined {
	const resolved = withBase(path);
	if (!resolved || resolved.startsWith('#') || hasProtocol(resolved)) {
		return resolved;
	}

	const [pathname, suffix] = splitSuffix(resolved);
	if (pathname === '/' || pathname.endsWith('/') || looksLikeFilePath(pathname)) {
		return resolved;
	}

	return `${pathname}/${suffix}`;
}

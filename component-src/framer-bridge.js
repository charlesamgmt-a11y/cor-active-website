// Framer editor-only controls are not needed on the public COR page.
// Animation code remains in the original components.
export const ControlType = new Proxy({}, {get: (_, name) => name});
export function addPropertyControls() {}
export function useIsStaticRenderer() { return false; }

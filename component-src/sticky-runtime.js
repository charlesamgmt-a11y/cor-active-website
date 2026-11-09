import React from 'react';
export * from 'framer-runtime';
export function useIsStaticRenderer() { return false; }
export function SmartComponentScopedContainer({children,className,style}) { return React.createElement('div',{className,style},children); }
export function ComponentViewportProvider({children}) { return children; }
export function useComponentViewport() { return undefined; }
export function getLoadingLazyAtYPosition() { return 'lazy'; }

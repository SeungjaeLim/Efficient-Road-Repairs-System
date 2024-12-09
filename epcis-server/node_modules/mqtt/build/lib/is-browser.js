"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const isBrowser = (typeof window !== 'undefined' && typeof window.document !== 'undefined') ||
    (typeof self === 'object' &&
        self.constructor &&
        self.constructor.name === 'DedicatedWorkerGlobalScope') ||
    (typeof navigator !== 'undefined' && navigator.product === 'ReactNative');
exports.default = isBrowser;
//# sourceMappingURL=is-browser.js.map
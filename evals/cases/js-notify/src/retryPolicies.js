// Delay (ms) before attempt n (1-based). Returning null means "stop retrying".
export const retryPolicies = {
  none: () => null,
  fixed: (attempt, { maxAttempts = 3, delay = 100 } = {}) =>
    attempt < maxAttempts ? delay : null,
  exponential: (attempt, { maxAttempts = 5, base = 50 } = {}) =>
    attempt < maxAttempts ? base * 2 ** (attempt - 1) : null,
};

export function getRetryPolicy(name) {
  const policy = retryPolicies[name];
  if (!policy) throw new Error(`Unknown retry policy: ${name}`);
  return policy;
}

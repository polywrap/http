module.exports = {
  roots: ["<rootDir>/src"],
  testMatch: ["**/?(*.)+(spec|test).+(ts|tsx|js)"],
  transform: {
    "^.+\\.(ts|tsx)$": "ts-jest",
  },
  modulePathIgnorePatterns: ["<rootDir>/src/__tests__/e2e/integration/"],
  testPathIgnorePatterns: [
    "<rootDir>/src/__tests__/e2e/integration/",
    "/.polywrap"
  ],
  transformIgnorePatterns: ["<rootDir>/src/__tests__/e2e/integration/"],
  testEnvironment: "node",
};

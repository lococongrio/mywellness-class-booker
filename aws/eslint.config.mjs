import typescriptEslint from "@typescript-eslint/eslint-plugin";
import eslintPluginPrettier from "eslint-plugin-prettier";
import prettier from "prettier";
import globals from "globals";
import tsParser from "@typescript-eslint/parser";
import path from "node:path";
import { fileURLToPath } from "node:url";
import js from "@eslint/js";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: js.configs.recommended,
  allConfig: js.configs.all,
});

export default [
  {
    files: ["**/*.ts", "**/*.tsx"],
    ignores: ["**/node_modules", "**/cdk.out", "**/*.d.ts"],
  },
  ...compat.extends(
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
  ),
  {
    plugins: {
      "@typescript-eslint": typescriptEslint,
      "eslint-plugin-prettier": eslintPluginPrettier,
      prettier: prettier,
    },

    languageOptions: {
      globals: {
        ...globals.node,
        ...globals.jest,
      },

      parser: tsParser,
      ecmaVersion: "latest",
      sourceType: "module",
    },

    rules: {
      "import/prefer-default-export": "off",
      "no-new": "off",
    },
  },
];

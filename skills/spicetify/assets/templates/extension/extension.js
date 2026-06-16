(async function spicetifyAgentTemplateExtension() {
  while (!window.Spicetify?.Platform) {
    await new Promise((resolve) => setTimeout(resolve, 100));
  }

  const storageKey = "spicetify-agent-template-enabled";
  if (!window.localStorage.getItem(storageKey)) {
    window.localStorage.setItem(storageKey, "true");
  }
})();

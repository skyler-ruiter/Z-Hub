// Public contributions always belong in the canonical repository, even when the
// site is built from a development fork.
export const githubRepo = 'guoxiliu/Z-Hub';

export function githubIssueUrl(template) {
  const url = new URL(`https://github.com/${githubRepo}/issues/new`);
  if (template) url.searchParams.set('template', template);
  return url.href;
}

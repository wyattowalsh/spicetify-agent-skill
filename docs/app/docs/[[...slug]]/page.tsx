import type { ReactNode } from "react";

import { notFound } from "next/navigation";

import { getContentMap, listDocsPages, readDocsPage } from "../../../lib/content";

type PageProps = {
  params: Promise<{
    slug?: string[];
  }>;
};

function inlineCode(text: string): ReactNode[] {
  return text.split(/(`[^`]+`)/g).map((part, index) => {
    if (part.startsWith("`") && part.endsWith("`")) {
      return <code key={index}>{part.slice(1, -1)}</code>;
    }
    return part;
  });
}

function renderMarkdown(markdown: string): ReactNode[] {
  const nodes: ReactNode[] = [];
  const lines = markdown.split("\n");
  let index = 0;

  while (index < lines.length) {
    const line = lines[index]?.trimEnd() ?? "";
    if (!line.trim()) {
      index += 1;
      continue;
    }

    if (line.startsWith("```")) {
      const language = line.slice(3).trim();
      const code: string[] = [];
      index += 1;
      while (index < lines.length && !lines[index]?.startsWith("```")) {
        code.push(lines[index] ?? "");
        index += 1;
      }
      index += 1;
      nodes.push(
        <pre key={`code-${index}`}>
          <code data-language={language || undefined}>{code.join("\n")}</code>
        </pre>,
      );
      continue;
    }

    const heading = /^(#{1,3})\s+(.+)$/.exec(line);
    if (heading) {
      const level = heading[1].length;
      const text = inlineCode(heading[2]);
      if (level === 1) {
        nodes.push(<h1 key={`h1-${index}`}>{text}</h1>);
      } else if (level === 2) {
        nodes.push(<h2 key={`h2-${index}`}>{text}</h2>);
      } else {
        nodes.push(<h3 key={`h3-${index}`}>{text}</h3>);
      }
      index += 1;
      continue;
    }

    if (line.startsWith("|")) {
      const tableLines: string[] = [];
      while (index < lines.length && lines[index]?.trim().startsWith("|")) {
        tableLines.push(lines[index]?.trim() ?? "");
        index += 1;
      }
      const [headerLine, separatorLine, ...rowLines] = tableLines;
      const headers = headerLine
        .split("|")
        .slice(1, -1)
        .map((cell) => cell.trim());
      const rows = (separatorLine?.includes("---") ? rowLines : tableLines.slice(1)).map((row) =>
        row
          .split("|")
          .slice(1, -1)
          .map((cell) => cell.trim()),
      );
      nodes.push(
        <div className="table-scroll" key={`table-${index}`}>
          <table>
            <thead>
              <tr>
                {headers.map((header) => (
                  <th key={header}>{inlineCode(header)}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {row.map((cell, cellIndex) => (
                    <td key={cellIndex}>{inlineCode(cell)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>,
      );
      continue;
    }

    if (line.startsWith("- ")) {
      const items: string[] = [];
      while (index < lines.length && lines[index]?.trim().startsWith("- ")) {
        items.push((lines[index] ?? "").trim().slice(2));
        index += 1;
      }
      nodes.push(
        <ul key={`ul-${index}`}>
          {items.map((item) => (
            <li key={item}>{inlineCode(item)}</li>
          ))}
        </ul>,
      );
      continue;
    }

    const paragraph: string[] = [line.trim()];
    index += 1;
    while (
      index < lines.length &&
      lines[index]?.trim() &&
      !lines[index]?.startsWith("#") &&
      !lines[index]?.trim().startsWith("- ") &&
      !lines[index]?.trim().startsWith("|") &&
      !lines[index]?.startsWith("```")
    ) {
      paragraph.push((lines[index] ?? "").trim());
      index += 1;
    }
    nodes.push(<p key={`p-${index}`}>{inlineCode(paragraph.join(" "))}</p>);
  }

  return nodes;
}

export function generateStaticParams() {
  return listDocsPages().map((page) => ({
    slug: page.slug ? page.slug.split("/") : [],
  }));
}

export default async function DocsPageRoute({ params }: PageProps) {
  const slug = (await params).slug?.join("/") ?? "";
  let page;
  try {
    page = readDocsPage(slug);
  } catch {
    notFound();
  }
  const contentMap = getContentMap();

  return (
    <main className="page docs-layout">
      <aside aria-label="Docs navigation">
        {contentMap.sections.map((section) => (
          <nav key={section.slug}>
            <h2>{section.title}</h2>
            <ul>
              {section.pages.map((entry) => {
                const href = entry === "index" ? "/docs" : `/docs/${entry}`;
                return (
                  <li key={entry}>
                    <a href={href}>{entry === "index" ? "/spicetify" : entry}</a>
                  </li>
                );
              })}
            </ul>
          </nav>
        ))}
      </aside>
      <article className="doc-article">
        <p className="eyebrow">{page.sourcePath}</p>
        <p>{page.description}</p>
        {renderMarkdown(page.body)}
      </article>
    </main>
  );
}


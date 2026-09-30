%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%
%% KI Textbook Class.
%%
%% Class for writing textbooks at Computer Science department
%% at Faculty of Electrotechnics and Informatics
%% and Technical University
%% of Košice.
%%
%% department homepage: http://kpi.fei.tuke.sk
%% project homepage:
%%
%%%%%
% \NeedsTeXFormat{LaTeX2e}
\ProvidesClass{kitextbook}[2021/08/06 KI Textbook Class, v2021.1]

% based on book class
\PassOptionsToClass{a5paper,10pt,twoside}{book}
\LoadClass{book}

% document geometry
\RequirePackage[
    a5paper,
    twoside,
    % top=20mm,
    % bottom=15mm,
    % textwidth=115mm,
    % inner=13mm,
    % outer=15mm,
    marginparwidth=0mm,
    marginparsep=0mm,
    hmargin={15mm,15mm},  % outer, inner
    vmargin={20mm,15mm}  % top, bottom
]{geometry}
% \RequirePackage{showframe} % for geometry debug options

\RequirePackage{fancyhdr}
\fancyhf{}
\fancyhead[RE]{\slshape \nouppercase{\leftmark}}
\fancyhead[LO]{\slshape \nouppercase{\rightmark}}
\fancyhead[RO,LE]{\slshape \thepage}

% TODO prerobit cez babel
\renewcommand{\@chapapp}{Prednáška}
\renewcommand{\chaptername}{Paper}

% titlesec for modification of chapter
\RequirePackage{titlesec}
\titleformat{\chapter}[display]
    {\bfseries\huge} % format
    {\large Prednáška \thechapter} % label before
    {0mm} % vertical separator (length)
    {} % before code
    [{\titlerule[0.07em]}] % after code

% additional packages
\RequirePackage{pdfpages}
\RequirePackage{fontspec}
\RequirePackage{pageslts}
\setmainfont{TeX Gyre Pagella}[
    % Numbers=OldStyle,
]

\RequirePackage{hyperref} % Required for hyperlinks
\RequirePackage{bookmark} % Required for pdf bookmarks
\PassOptionsToPackage{hyphens}{url} % Break long URLs and use hyphens to separate the pieces

\hypersetup{
%    unicode,
   pdfusetitle,
   %pdfusekeywords,
   pdftoolbar=true,
   pdfmenubar=true,
   pdfwindowui=true,
   bookmarksopenlevel={0},
   bookmarksnumbered,
   bookmarksopen,
   pdfhighlight={/P},
%    colorlinks=true,
%    linkcolor=magenta,
%    filecolor=magenta,
%    urlcolor=magenta,
%    citecolor=magenta,
   baseurl={https://kpi.fei.tuke.sk/}
}

\RequirePackage{graphicx}
\DeclareGraphicsExtensions{.pdf,.png,.jpg,.eps}


% environments
\RequirePackage[skins,breakable]{tcolorbox}

\newtcolorbox{warningbox}[1]{
    enhanced,
    borderline north={2pt}{0pt}{red!7!white},
    borderline south={2pt}{0pt}{red!7!white},
    borderline east={2pt}{0pt}{red!75!black},
    borderline west={2pt}{0pt}{red!75!black},
    colback=red!7!white,
    frame hidden,
    boxsep=1em,
    breakable
}

\newtcolorbox{infobox}[1]{
    enhanced,
    borderline north={2pt}{0pt}{cyan!7!white},
    borderline south={2pt}{0pt}{cyan!7!white},
    borderline east={2pt}{0pt}{cyan!75!black},
    borderline west={2pt}{0pt}{cyan!75!black},
    colback=cyan!7!white,
    frame hidden,
    boxsep=1em,
    breakable
}


%%% Numeric citations and sorting by year (descending), name and title
% \RequirePackage{csquotes}
% \RequirePackage[
%     bibencoding=auto,
%     babel=other,
%     % style=iso-numeric,   % old numeric system
%     % style=iso-authoryear,   % support for ISO 690
%     sortlocale=sk_SK,       % sorts entries based on slovak locale
%     autolang=other,
%     sorting=ydnt,           % from latest to oldest
%     backend=biber           % different backend
% ]{biblatex}

\renewcommand{\title}[1]{
	\gdef\@title{#1} % Store the full title in @title
	\hypersetup{pdftitle={#1}} % Set the PDF metadata title
}

\newcommand{\subtitle}[1]{
	\gdef\@subtitle{#1} % Store the subtitle in @subtitle
    % \hypersetup{pdfinfo={Subtitle={#1}}}
}

\newcommand{\isbn}[1]{
	\gdef\@isbn{#1} % Store the ISBN in @isbn
}

\renewcommand{\thanks}[1]{
    \gdef\@thanks{#1}
}

\renewcommand{\frontmatter}{%
    \cleardoublepage
    \pagestyle{empty}
    % \pagenumbering{arabic}
    \@mainmatterfalse
}

\renewcommand\mainmatter{%
    \cleardoublepage
    \pagestyle{fancy}
    \@mainmattertrue
}

\renewcommand\backmatter{%
  \if@openright
    \cleardoublepage
  \else
    \clearpage
  \fi
  \@mainmatterfalse
}

% make empty default title
\renewcommand\maketitle{}

\AtBeginDocument{
    \pagenumbering{arabic}
    \pagestyle{empty}

    % cover and blank page
    \includepdf{resources/front.cover.a4}
    \cleardoublepage

    % patitul
    \vspace*{2cm}
    \begin{center}
        \@title
    \end{center}
    \cleardoublepage

    % titlepage
    \titlepage
    \impressum
}

\AtEndDocument{
    \pagestyle{empty}
    \cleardoublepage

    \ifodd\thepage
        \null
        \clearpage
    \fi

    % tiraz
    \newpage
    \vglue0pt\vfill

    {
        \setlength{\parindent}{0cm}

        \@author

        \smallskip

        {\Huge \textbf{\@title}}\\
        {\large \textbf{\@subtitle}}

        \bigskip

        Vydala Technická univerzita v Košiciach, Letná 9, 042 00 Košice, Slovensko\\
        \texttt{\url{http://www.tuke.sk}}

        \noindent Vydanie: prvé\\
        \noindent Náklad: 50 ks\\
        \noindent Rozsah: \lastpageref{VeryLastPage} strán\\
        \noindent Rok: 2021

        \bigskip

        Sadzba typografickým systémom \LaTeX.\\
        ISBN \@isbn
    }

    % endpage
    \pagebreak
    \null
    \clearpage

    \includepdf{resources/back.cover.a4}
    % \vglue 0pt\vfill

    % \begin{center}
    %     ISBN \@isbn
    % \end{center}
}

\renewcommand{\titlepage}{
    \thispagestyle{empty}

    \vspace*{5cm}

    \begin{center}
        {\Huge \textbf{\@title}}

        \smallskip

        {\large {\@subtitle}}

        \bigskip

        {\textbf \@author}

        \vfill

        \includegraphics[width=3cm]{images/logo.kpi}
    \end{center}

    \newpage
}

\newcommand{\impressum}{
    % \thispagestyle{empty}
    \vglue 0pt\vfill

    {
        \setlength{\parindent}{0cm}

        \textbf{\large \@title}\\
        \@subtitle\\
        \@author

        \bigskip

        \textbf{Vydavateľ:}\\
        Technická univerzita v Košiciach\\
        Letná 9, 042 00 Košice, Slovensko\\
        \url{www.tuke.sk}\\
        Katedra počítačov a informatiky\\
        \url{www.kpi.fei.tuke.sk}

        \bigskip

        % \textbf{Odborná korekcia:}\\
        % Marek Pohančeník

        \bigskip

        prvé vydanie, Košice \@date\\
        ISBN \@isbn

        \bigskip

        $\copyright${} \@date{} \@author

        \bigskip

        Obálku ilustrovala $\copyright${} Janka Slebodníková, \url{www.maranveart.com}. Ilustrácia bola prvýkrát publikovaná v komixoch autorky, ktoré vychádzali v rokoch 2014 až 2018 na stránkach portálu \url{www.root.cz}.

        \bigskip

        \@thanks

        \bigskip


        Toto autorské dielo podlieha medzinárodnej licencii \textit{Creative Commons BY-NC-SA 4.0}. To znamená, že:

        \begin{itemize}
            \item toto dielo môžete ďalej voľne šíriť a upravovať za predpokladu, že uvediete pôvod diela
            \item ak budete toto dielo upravovať, musíte svoje odvodené dielo publikovať pod rovnakou licenciou ako pôvodné dielo
            \item toto dielo je zakázané používať pre komerčné účely
        \end{itemize}

        \includegraphics{../images/cc-by-nc-sa.png}
    }

    \pagebreak
}


// Global display name mapping for problem clusters
const overviewClusterNameMap = {
  "face_grouping_people_identification_breakdown": "People identification failure",
  "semantic_ai_natural_language_query_mismatch": "Mismatch between user query and search response",
  "temporal_chronological_discovery_gap": "Failures in date & time based search",
  "visual_attribute_object_detail_retrieval_friction": "Failure in object & visual attribute based photo search",
  "result_overload_and_refinement_exhaustion": "Users drown in results, struggle to narrow down",
  "text_document_screenshot_ocr_breakdown": "Failures in text, document, screenshot search"
};

document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  initNavigation();
  renderOverview();
  renderClusters();
  renderAnalyticalQuestions();
  renderOpportunities();
  initModal();
});

// --------------------------------------------------------------------------
// 1. Theme Management (Light / Dark Fluent 2)
// --------------------------------------------------------------------------
function initTheme() {
  const toggleBtn = document.getElementById("theme-toggle-btn");
  const themeIcon = document.getElementById("theme-icon");
  const isDark = localStorage.getItem("gphotos_theme") === "dark";

  if (isDark) {
    document.body.classList.add("dark-theme");
    themeIcon.textContent = "☀️";
  }

  toggleBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark-theme");
    const activeDark = document.body.classList.contains("dark-theme");
    localStorage.setItem("gphotos_theme", activeDark ? "dark" : "light");
    themeIcon.textContent = activeDark ? "☀️" : "🌙";
  });
}

// --------------------------------------------------------------------------
// 2. Navigation Tab Switching (Fluent 2 Pivot Tabs)
// --------------------------------------------------------------------------
function initNavigation() {
  const tabs = document.querySelectorAll(".nav-tab");
  const panels = document.querySelectorAll(".view-panel");

  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      const targetId = tab.getAttribute("data-tab");

      tabs.forEach(t => {
        t.classList.remove("active");
        t.setAttribute("aria-selected", "false");
      });
      panels.forEach(p => p.classList.remove("active"));

      tab.classList.add("active");
      tab.setAttribute("aria-selected", "true");
      const targetPanel = document.getElementById(targetId);
      if (targetPanel) {
        targetPanel.classList.add("active");
      }
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });
}

function switchToTab(tabId) {
  const targetTab = document.querySelector(`.nav-tab[data-tab="${tabId}"]`);
  if (targetTab) {
    targetTab.click();
  }
}

// --------------------------------------------------------------------------
// 3. Render View 1: Overview Analytics
// --------------------------------------------------------------------------
function renderOverview() {
  if (typeof METRICS_DATA === "undefined") return;

  const kpis = METRICS_DATA.dataset_kpis;
  const outcomes = METRICS_DATA.search_retrieval_outcomes;
  const failureStages = METRICS_DATA.failure_stages_funnel;
  const rememberedClues = METRICS_DATA.remembered_clues_distribution;
  const sources = kpis.sources_breakdown;

  // Set Key Takeaway
  const takeawayEl = document.getElementById("key-takeaway-text");
  if (takeawayEl && METRICS_DATA.key_takeaway) {
    takeawayEl.innerHTML = METRICS_DATA.key_takeaway;
  }

  // 1. KPI Cards
  const kpiGrid = document.getElementById("overview-kpi-grid");
  if (kpiGrid) {
    kpiGrid.innerHTML = `
      <div class="kpi-card">
        <div class="kpi-label">Total Ingested</div>
        <div class="kpi-value" style="color: var(--color-danger);">${kpis.total_raw_conversations}</div>
        <div class="kpi-meta">Across 6 Public Channels</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Cleaned & Normalised</div>
        <div class="kpi-value" style="color: var(--color-purple);">${kpis.total_normalized_conversations}</div>
        <div class="kpi-meta">${kpis.total_duplicates_spam_removed} duplicates/spam removed</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Relevant Reviews</div>
        <div class="kpi-value" style="color: var(--color-primary);">${kpis.total_relevant_conversations}</div>
        <div class="kpi-meta">Talks about photo retrieval</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Irrelevant Excluded</div>
        <div class="kpi-value" style="color: var(--color-info);">${kpis.total_irrelevant_conversations}</div>
        <div class="kpi-meta">Billing, login & non-search issues</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Authentic User Voice</div>
        <div class="kpi-value" style="color: var(--color-success);">${kpis.authentic_records_percentage}%</div>
        <div class="kpi-meta">0% Synthetic Reviews</div>
      </div>
    `;
  }

  // 2. Outcomes Breakdown
  const outcomesList = document.getElementById("outcomes-breakdown-list");
  if (outcomesList) {
    const outcomeDisplayNames = {
      "Failure": "Failure",
      "Success": "Success",
      "Partial Success": "Partial Success",
      "Unknown": "Not indicative"
    };

    const fillClasses = {
      "Failure": "fill-danger",
      "Unknown": "fill-muted",
      "Success": "fill-success",
      "Partial Success": "fill-warning"
    };

    outcomesList.innerHTML = outcomes.map(o => {
      const displayName = outcomeDisplayNames[o.outcome] || o.outcome;
      return `
      <div class="progress-item">
        <div class="progress-header">
          <span class="progress-title">${displayName}</span>
          <span class="progress-stats">${o.percentage}%</span>
        </div>
        <div class="progress-track">
          <div class="progress-fill ${fillClasses[o.outcome] || 'fill-primary'}" style="width: ${o.percentage}%"></div>
        </div>
      </div>
    `;
    }).join("");
  }

  // 3. Failure Funnel
  const failureFunnelList = document.getElementById("failure-funnel-list");
  if (failureFunnelList) {
    const stageDisplayNames = {
      "1. Translation Struggle": "User doesn't know what to type",
      "2. System Retrieval Failure": "System fails to find or recognize the photo",
      "3. Result Overload / Distinction": "Too many photos to choose from",
      "4. Refinement Breakdown": "No helpful filters to narrow down search",
      "Not Indicative": "Not indicative of the journey"
    };

    const stageFillClasses = {
      "1. Translation Struggle": "fill-purple",
      "2. System Retrieval Failure": "fill-danger",
      "3. Result Overload / Distinction": "fill-warning",
      "4. Refinement Breakdown": "fill-info",
      "Not Indicative": "fill-muted"
    };

    failureFunnelList.innerHTML = failureStages.map(s => {
      const displayName = stageDisplayNames[s.failure_stage] || s.failure_stage;
      return `
      <div class="progress-item">
        <div class="progress-header">
          <span class="progress-title">${displayName}</span>
          <span class="progress-stats">${s.percentage}%</span>
        </div>
        <div class="progress-track">
          <div class="progress-fill ${stageFillClasses[s.failure_stage] || 'fill-primary'}" style="width: ${Math.max(s.percentage, s.count > 0 ? 3 : 0)}%"></div>
        </div>
      </div>
    `;
    }).join("");
  }

  // 4. Remembered Clues
  const cluesBars = document.getElementById("remembered-clues-bars");
  if (cluesBars) {
    cluesBars.innerHTML = rememberedClues.slice(0, 6).map(c => `
      <div class="progress-item">
        <div class="progress-header">
          <span class="progress-title">${c.dimension}</span>
          <span class="progress-stats">${c.percentage_of_relevant_conversations}%</span>
        </div>
        <div class="progress-track">
          <div class="progress-fill fill-primary" style="width: ${c.percentage_of_relevant_conversations}%"></div>
        </div>
      </div>
    `).join("");
  }

  // 5. Source Breakdown
  const sourcesList = document.getElementById("sources-breakdown-list");
  if (sourcesList) {
    const formatSourceName = (src) => {
      const names = {
        "google_play": "Google Play Store",
        "app_store": "Apple App Store",
        "google_help_community": "Google Help Community",
        "youtube": "YouTube Comments",
        "forums": "Public Tech Forums",
        "social": "Public Social / X"
      };
      return names[src] || src;
    };

    sourcesList.innerHTML = sources.map(s => `
      <div class="progress-item">
        <div class="progress-header">
          <span class="progress-title">${formatSourceName(s.source_name)}</span>
          <span class="progress-stats">${s.percentage_of_raw}%</span>
        </div>
        <div class="progress-track">
          <div class="progress-fill fill-purple" style="width: ${s.percentage_of_raw}%"></div>
        </div>
      </div>
    `).join("");
  }

  // 6. Quick Jump Clusters
  const quickClusters = document.getElementById("quick-clusters-grid");
  if (quickClusters && typeof CLUSTERS_DATA !== "undefined") {
    quickClusters.innerHTML = CLUSTERS_DATA.map((c, idx) => {
      const displayName = overviewClusterNameMap[c.cluster_id] || c.cluster_name;
      return `
      <div class="quick-cluster-card" onclick="switchToCluster('${c.cluster_id}')">
        <div>
          <div class="quick-cluster-top">
            <span class="cluster-rank-badge">#${idx + 1} Problem Cluster</span>
            <span style="font-weight: 700; color: var(--color-primary); font-size: 0.85rem;">(${c.conversation_count} convs)</span>
          </div>
          <h4 class="quick-cluster-title">${displayName}</h4>
          <p class="quick-cluster-desc">${c.cluster_description}</p>
        </div>
        <div class="quick-cluster-bottom">
          <span>Explore Qualitative Profile</span>
          <span>&rarr;</span>
        </div>
      </div>
    `;
    }).join("");
  }
}

// --------------------------------------------------------------------------
// 4. Render View 2: Problem Clusters Explorer
// --------------------------------------------------------------------------
function renderClusters(filter = "all", searchQuery = "") {
  const container = document.getElementById("problem-clusters-container");
  if (!container || typeof CLUSTERS_DATA === "undefined") return;

  const query = searchQuery.toLowerCase().trim();

  const filteredClusters = CLUSTERS_DATA.filter(c => {
    // Category filter
    let matchesCategory = true;
    if (filter === "people") matchesCategory = c.cluster_id.includes("people") || c.cluster_id.includes("face");
    else if (filter === "visual") matchesCategory = c.cluster_id.includes("visual") || c.cluster_id.includes("ocr");
    else if (filter === "time") matchesCategory = c.cluster_id.includes("temporal") || c.cluster_id.includes("date");
    else if (filter === "ai") matchesCategory = c.cluster_id.includes("ai") || c.cluster_id.includes("semantic");

    // Search query filter
    let matchesSearch = true;
    if (query) {
      const haystack = (c.cluster_name + " " + c.cluster_description + " " + c.common_memory_clues.join(" ") + " " + c.old_photos_characteristics).toLowerCase();
      matchesSearch = haystack.includes(query);
    }

    return matchesCategory && matchesSearch;
  });

  if (filteredClusters.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 3rem; background: var(--bg-surface); border-radius: var(--radius-lg); border: 1px solid var(--border-subtle);">
        <p style="color: var(--text-muted); font-size: 1rem;">No problem clusters matched your search criteria.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = filteredClusters.map((c, idx) => {
    const displayName = overviewClusterNameMap[c.cluster_id] || c.cluster_name;
    const quotesHtml = c.representative_evidence_quotes.map(q => `
      <div class="quote-bubble">
        "${q.quote}"
        <span class="quote-author">&mdash; ${q.author || 'User'} (${formatSourceName(q.source)})</span>
      </div>
    `).join("");

    const clueTags = c.common_memory_clues.map(cl => cl.trim() === "-" ? `<span style="color: var(--text-muted); font-size: 1.1rem; font-weight: 500;">-</span>` : `<span class="clue-tag">${cl}</span>`).join("");
    const missingTags = c.common_missing_clues.map(m => m.trim() === "-" ? `<span style="color: var(--text-muted); font-size: 1.1rem; font-weight: 500;">-</span>` : `<span class="missing-tag">${m}</span>`).join("");
    const behaviorTags = c.common_search_behaviors.map(b => b.trim() === "-" ? `<span style="color: var(--text-muted); font-size: 1.1rem; font-weight: 500;">-</span>` : `<span class="clue-tag">${b}</span>`).join("");

    return `
      <div class="cluster-card" id="cluster-card-${c.cluster_id}">
        <div class="cluster-card-header">
          <div class="cluster-title-wrap">
            <span class="cluster-rank-badge">#${idx + 1}</span>
            <h3 class="cluster-card-title">${displayName}</h3>
          </div>
        </div>

        <p class="cluster-description-text">${c.cluster_description}</p>

        <div class="cluster-attrs-grid">
          <div class="attr-block">
            <h5>What Users Remember</h5>
            <div class="tags-list">${clueTags}</div>
          </div>

          <div class="attr-block">
            <h5>WHAT USERS FORGET</h5>
            <div class="tags-list">${missingTags}</div>
          </div>

          <div class="attr-block">
            <h5>Observed Search Behaviors</h5>
            <div class="tags-list">${behaviorTags}</div>
          </div>

          <div class="attr-block">
            <h5>Affected Old Photos Context</h5>
            <p class="old-photos-text">${c.old_photos_characteristics}</p>
          </div>
        </div>

        <div class="cluster-quotes-box">
          <div class="quotes-heading">Representative Verbatim User Quotes</div>
          ${quotesHtml}
        </div>

        <div class="cluster-card-actions">
          <button class="btn-view-evidence" onclick="openSupportingConversations('${c.cluster_id}')">
            <span>💬</span>
            <span>View Supporting Conversations (${c.conversation_count})</span>
          </button>
        </div>
      </div>
    `;
  }).join("");

  // Setup search input and filter buttons
  setupClusterFilters();
}

function setupClusterFilters() {
  const searchInput = document.getElementById("cluster-search-input");
  const filterPills = document.querySelectorAll(".filter-pill");

  if (searchInput && !searchInput.dataset.initialized) {
    searchInput.dataset.initialized = "true";
    searchInput.addEventListener("input", (e) => {
      const activeFilter = document.querySelector(".filter-pill.active")?.getAttribute("data-filter") || "all";
      renderClusters(activeFilter, e.target.value);
    });
  }

  filterPills.forEach(pill => {
    if (!pill.dataset.initialized) {
      pill.dataset.initialized = "true";
      pill.addEventListener("click", () => {
        filterPills.forEach(p => p.classList.remove("active"));
        pill.classList.add("active");
        const filterVal = pill.getAttribute("data-filter");
        const searchVal = document.getElementById("cluster-search-input")?.value || "";
        renderClusters(filterVal, searchVal);
      });
    }
  });
}

function switchToCluster(clusterId) {
  switchToTab("view-clusters");
  setTimeout(() => {
    const card = document.getElementById(`cluster-card-${clusterId}`);
    if (card) {
      card.scrollIntoView({ behavior: "smooth", block: "center" });
      card.style.borderColor = "var(--color-primary)";
      card.style.boxShadow = "var(--shadow-lg)";
      setTimeout(() => {
        card.style.borderColor = "";
        card.style.boxShadow = "";
      }, 2000);
    }
  }, 250);
}

// --------------------------------------------------------------------------
// 5. Render View 3: 10 Key Analytical Questions
// --------------------------------------------------------------------------
function renderAnalyticalQuestions() {
  const accordion = document.getElementById("analytical-questions-accordion");
  if (!accordion || typeof ANALYTICAL_QUESTIONS_DATA === "undefined") return;

  accordion.innerHTML = ANALYTICAL_QUESTIONS_DATA.map((q, idx) => {
    const findingsHtml = q.findings.map(f => `
      <div class="finding-item">
        <div class="finding-title">${f.archetype}</div>
        <div class="finding-desc">${f.description}</div>
      </div>
    `).join("");

    return `
      <div class="question-card ${idx === 0 ? 'open' : ''}" id="question-card-${q.id}">
        <div class="question-header" onclick="toggleQuestion('question-card-${q.id}')">
          <span class="question-num-tag">Q${q.number}</span>
          <h3 class="question-title">${q.question}</h3>
          <span class="accordion-chevron">▼</span>
        </div>
        <div class="question-body">
          ${q.summary ? `<p class="question-summary">${q.summary}</p>` : ''}
          <div class="findings-grid">${findingsHtml}</div>
          <div class="metric-callout-pill">
            <span style="${q.icon === '*' ? 'font-size: 1.1rem; font-weight: 800; line-height: 1;' : ''}">${q.icon || '📊'}</span>
            <span>${q.metric_callout}</span>
          </div>
        </div>
      </div>
    `;
  }).join("");
}

function toggleQuestion(cardId) {
  const card = document.getElementById(cardId);
  if (card) {
    card.classList.toggle("open");
  }
}

// --------------------------------------------------------------------------
// 6. Render View 4: Opportunity Hypotheses
// --------------------------------------------------------------------------
function renderOpportunities() {
  const container = document.getElementById("opportunity-cards-container");
  if (!container || typeof OPPORTUNITIES_DATA === "undefined") return;

  container.innerHTML = OPPORTUNITIES_DATA.map((opp, idx) => {
    const researchQuestions = opp.open_research_questions.map(rq => `<li>${rq}</li>`).join("");

    return `
      <div class="opportunity-card" id="opp-card-${opp.opportunity_id}">
        <div class="opportunity-top">
          <div class="opp-badge-row">
            <span class="cluster-rank-badge">Hypothesis #${idx + 1}</span>
            <span class="opp-freq-pill">${opp.frequency.conversation_count} Conversations (${opp.frequency.percentage_of_relevant_conversations}%)</span>
            <span class="opp-stage-pill">${opp.affected_retrieval_stage}</span>
          </div>

          <h3 class="opp-title">${opp.problem_title}</h3>
          <p class="opp-desc">${opp.problem_description}</p>

          <div class="opp-segment-box">
            <div class="opp-segment-label">Affected User Segment & Situation</div>
            <div class="opp-segment-value">${opp.affected_segment}</div>
          </div>

          <div class="opp-why-matters">
            <span class="opp-why-label">Why Successful Retrieval Matters: </span>
            <span>${opp.why_successful_retrieval_matters}</span>
          </div>
        </div>

        <div class="research-questions-box">
          <div class="rq-header">
            <span>🔬</span>
            <span>Qualitative Research Questions for User Interviews</span>
          </div>
          <ol class="rq-list">${researchQuestions}</ol>
        </div>
      </div>
    `;
  }).join("");
}

// --------------------------------------------------------------------------
// 7. Modal: Supporting Conversations Viewer
// --------------------------------------------------------------------------
let currentClusterRecordIds = [];

function initModal() {
  const modal = document.getElementById("conversations-modal");
  const closeBtn = document.getElementById("modal-close-btn");
  const searchInput = document.getElementById("modal-filter-input");

  if (closeBtn) {
    closeBtn.addEventListener("click", closeModal);
  }

  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        closeModal();
      }
    });
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeModal();
    }
  });

  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      filterModalConversations(e.target.value);
    });
  }
}

function openSupportingConversations(clusterId) {
  if (typeof CLUSTERS_DATA === "undefined" || typeof EXTRACTIONS_MAP === "undefined") return;

  const cluster = CLUSTERS_DATA.find(c => c.cluster_id === clusterId);
  if (!cluster) return;

  const modal = document.getElementById("conversations-modal");
  const titleEl = document.getElementById("modal-cluster-title");
  const countEl = document.getElementById("modal-conversation-count");
  const searchInput = document.getElementById("modal-filter-input");

  const displayName = overviewClusterNameMap[cluster.cluster_id] || cluster.cluster_name;
  if (titleEl) titleEl.textContent = displayName;
  if (countEl) countEl.textContent = `${cluster.conversation_count} Supporting User Reviews`;
  if (searchInput) searchInput.value = "";

  currentClusterRecordIds = cluster.member_record_ids || [];
  renderModalReviews(currentClusterRecordIds);

  if (modal) {
    modal.classList.remove("hidden");
    document.body.style.overflow = "hidden";
  }
}

function renderModalReviews(recordIds) {
  const listEl = document.getElementById("modal-conversations-list");
  if (!listEl) return;

  if (recordIds.length === 0) {
    listEl.innerHTML = `<p style="text-align: center; color: var(--text-muted); padding: 2rem;">No matching conversations found.</p>`;
    return;
  }

  listEl.innerHTML = recordIds.map(rid => {
    const rec = EXTRACTIONS_MAP[rid];
    if (!rec) return "";

    const author = rec.author_identifier || "Verified Public User";
    const source = formatSourceName(rec.source);
    const date = rec.date ? new Date(rec.date).toLocaleDateString("en-US", { year: 'numeric', month: 'short', day: 'numeric' }) : "Recent";
    const rating = rec.rating ? "★".repeat(rec.rating) + "☆".repeat(5 - rec.rating) : "";
    const text = rec.original_text || rec.cleaned_text || "";
    const outcomeMap = {
      "Failure": "Failure",
      "Success": "Success",
      "Partial Success": "Partial Success",
      "Unknown": "Not indicative"
    };
    const outcome = outcomeMap[rec.retrieval_outcome?.outcome] || rec.retrieval_outcome?.outcome || "Unknown";

    const stageMap = {
      "1. Translation Struggle": "User doesn't know what to type",
      "2. System Retrieval Failure": "System fails to find or recognize the photo",
      "3. Result Overload / Distinction": "Too many photos to choose from",
      "4. Refinement Breakdown": "No helpful filters to narrow down search",
      "Not Indicative": "Not indicative of the journey"
    };
    const rawStage = rec.failure_breakdown?.failure_stage || "Not Indicative";
    const stage = stageMap[rawStage] || rawStage;

    // Format extracted clues
    const clues = rec.remembered_clues || [];
    const clueBadges = clues.map(c => `
      <div class="evidence-span-box">
        <span class="evidence-span-label">Extracted ${c.dimension.toUpperCase()} Clue:</span>
        "${c.verbatim_evidence_span}"
      </div>
    `).join("");

    return `
      <div class="review-card">
        <div class="review-card-header">
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span class="review-author">${author}</span>
            <span style="color: var(--color-warning); font-size: 0.85rem;">${rating}</span>
          </div>
          <span class="review-source-tag">${source}</span>
        </div>
        <div class="review-meta">
          <span>Date: ${date}</span> &bull; 
          <span>Outcome: <strong>${outcome}</strong></span> &bull;
          <span>Stage: <strong>${stage}</strong></span>
        </div>
        <p class="review-verbatim-text">"${text}"</p>
        ${clueBadges}
      </div>
    `;
  }).join("");
}

function filterModalConversations(query) {
  const q = query.toLowerCase().trim();
  if (!q) {
    renderModalReviews(currentClusterRecordIds);
    return;
  }

  const matchingIds = currentClusterRecordIds.filter(rid => {
    const rec = EXTRACTIONS_MAP[rid];
    if (!rec) return false;
    const haystack = (rec.original_text + " " + (rec.author_identifier || "") + " " + rec.source).toLowerCase();
    return haystack.includes(q);
  });

  renderModalReviews(matchingIds);
}

function closeModal() {
  const modal = document.getElementById("conversations-modal");
  if (modal) {
    modal.classList.add("hidden");
    document.body.style.overflow = "";
  }
}

// --------------------------------------------------------------------------
// Helpers
// --------------------------------------------------------------------------
function formatSourceName(src) {
  const names = {
    "google_play": "Google Play",
    "app_store": "App Store",
    "google_help_community": "Help Community",
    "youtube": "YouTube",
    "forums": "Public Forum",
    "social": "Public Social"
  };
  return names[src] || src;
}

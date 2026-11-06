این صفحه همه فرمول‌ها و مفاهیم اصلی درس را در قالب کارت‌های کوتاه جمع کرده است. هر کارت به جلسه‌ای پیوند دارد که مطلب در آن به تفصیل آمده است. نمادها همان نمادهای جزوه‌اند: $\Prob$ برای احتمال، $\E$ برای میانگین، $\Phi$ برای CDF گاوسی استاندارد (در بخش تابع مشخصه، $\Phi_X(\omega)$ تابع مشخصه است).

## مبانی احتمال

### مجموعه‌ها و شمارش

::: {.card t="قوانین دمورگان" ref="0:s1"}
$$\Big(\bigcup_i A_i\Big)^c=\bigcap_i A_i^c,\qquad \Big(\bigcap_i A_i\Big)^c=\bigcup_i A_i^c$$
:::

::: {.card t="اصل ضرب و جایگشت" ref="0:s2"}
$$|A_1\times\cdots\times A_k|=|A_1|\cdots|A_k|$$

تعداد ترتیب‌های $n$ شیء: $n!$. انتخاب **مرتب** $k$ از $n$: $\dfrac{n!}{(n-k)!}$.
:::

::: {.card t="ترکیب و بسط دوجمله‌ای" ref="0:s2"}
$$\binom nk=\frac{n!}{k!\,(n-k)!},\qquad (x+y)^n=\sum_{k=0}^n\binom nk x^ky^{n-k}$$

ضریب چندجمله‌ای: $\dbinom{n}{k_1,\ldots,k_r}=\dfrac{n!}{k_1!\cdots k_r!}$ با $\sum k_i=n$.
:::

::: {.card t="ستاره و میله" ref="0:s2"}
تعداد جواب‌های صحیح **نامنفی** $x_1+\cdots+x_k=n$:
$$\binom{n+k-1}{k-1}$$

با شرط $x_i\ge1$: $\dbinom{n-1}{k-1}$.
:::

### فضای احتمال و اصول کولموگروف

::: {.card t="فضای احتمال و اصول کولموگروف" ref="0:s3"}
سه‌تایی $(\Omega,\F,\Prob)$ با:

1. $\Prob(A)\ge0$
2. $\Prob(\Omega)=1$
3. برای رویدادهای دوبه‌دو ناسازگار: $\Prob\big(\bigcup_i A_i\big)=\sum_i\Prob(A_i)$
:::

::: {.card t="نتایج مستقیم اصول" ref="3:s2"}
$$\Prob(\varnothing)=0,\qquad \Prob(A^c)=1-\Prob(A)$$
$$A\subseteq B\ \Rightarrow\ \Prob(A)\le\Prob(B)$$
$$\Prob(A\cup B)=\Prob(A)+\Prob(B)-\Prob(A\cap B)$$
:::

::: {.card t="اصل شمول و عدم شمول" ref="3:s3"}
$$\begin{aligned}\Prob\Big(\bigcup_{i=1}^nE_i\Big)={}&\sum_i\Prob(E_i)-\sum_{i<j}\Prob(E_iE_j)+\sum_{i<j<k}\Prob(E_iE_jE_k)\\&-\cdots+(-1)^{n+1}\Prob(E_1\cdots E_n)\end{aligned}$$
:::

::: {.card t="کران اجتماع (نامساوی بول)" ref="3:s4"}
$$\Prob\Big(\bigcup_iE_i\Big)\le\sum_i\Prob(E_i)$$

برای رویدادهای کم‌احتمال، تقریب خوبی است.
:::

::: {.card t="فضای نمونه متناهی" ref="3:s5"}
$$\Prob(A)=\sum_{\omega\in A}p(\omega)$$

اگر همه نتایج هم‌احتمال باشند: $\Prob(A)=\dfrac{|A|}{|\Omega|}$.
:::

### آزمایش برنولی و استقلال

::: {.card t="آزمایش برنولی تکرارشونده" ref="3:s6"}
احتمال دقیقاً $k$ موفقیت در $n$ آزمایش مستقل:
$$\Prob(k)=\binom nk p^k(1-p)^{n-k}$$
:::

::: {.card t="پدیده تمرکز" ref="3:s6-1"}
برای سکه سالم، جرم احتمال در بازه‌ای به عرض $O(\sqrt n)$ حول $n/2$ جمع می‌شود و ارتفاع قله $O(n^{-1/2})$ است:
$$\binom{n}{n/2}2^{-n}\approx\sqrt{\frac{2}{\pi n}},\qquad m!\approx\sqrt{2\pi m}\Big(\frac me\Big)^m$$
:::

::: {.card t="استقلال دو رویداد" ref="3:s7"}
$$\Prob(A\cap B)=\Prob(A)\,\Prob(B)\ \iff\ \Prob(A\given B)=\Prob(A)$$

اگر $A,B$ مستقل باشند، $A^c,B$ و $A^c,B^c$ هم مستقل‌اند. دو رویداد ناسازگار با احتمال مثبت، **وابسته**‌اند.
:::

::: {.card t="استقلال چند رویداد" ref="3:s7"}
برای **هر** زیرمجموعه $S$ از اندیس‌ها:
$$\Prob\Big(\bigcap_{i\in S}A_i\Big)=\prod_{i\in S}\Prob(A_i)$$

استقلال دوبه‌دو، استقلال کامل را نتیجه نمی‌دهد.
:::

::: {.card t="دو نتیجه مشهور" ref="3:s8-2 3:s8-3"}
**روز تولد:** احتمال اینکه از $n$ نفر هیچ دو نفری هم‌تولد نباشند:
$$\prod_{i=0}^{n-1}\Big(1-\frac{i}{365}\Big)\approx e^{-n(n-1)/730}$$

برای $n=23$ احتمال هم‌تولدی $\approx0.507$ است. **مونتی هال:** با عوض کردن در، احتمال برد $\frac23$ است.
:::

### احتمال شرطی و قانون بیز

::: {.card t="احتمال شرطی" ref="4:s1"}
$$\Prob(A\given B)=\frac{\Prob(A\cap B)}{\Prob(B)},\qquad \Prob(B)>0$$

$\Prob(\cdot\given B)$ خودش یک اندازه احتمال است.
:::

::: {.card t="قانون زنجیره‌ای" ref="4:s2"}
$$\Prob(A_1\cdots A_n)=\Prob(A_1)\,\Prob(A_2\given A_1)\cdots\Prob(A_n\given A_1\cdots A_{n-1})$$
:::

::: {.card t="قانون احتمال کل" ref="4:s3"}
اگر $A_1,\ldots,A_n$ افرازی از $\Omega$ باشند:
$$\Prob(E)=\sum_{i=1}^n\Prob(E\given A_i)\,\Prob(A_i)$$
:::

::: {.card t="قانون بیز" ref="4:s4"}
$$\Prob(A_j\given E)=\frac{\Prob(E\given A_j)\,\Prob(A_j)}{\sum_i\Prob(E\given A_i)\,\Prob(A_i)}$$

$\text{پسین}\propto\text{درست‌نمایی}\times\text{پیشین}$
:::

::: {.card t="استقلال شرطی" ref="4:s5 5:s1"}
$$\Prob(A\cap B\given C)=\Prob(A\given C)\,\Prob(B\given C)$$

استقلال شرطی و استقلال هیچ‌کدام دیگری را نتیجه نمی‌دهند. برای متغیر پنهان $C$: $\Prob(B\given A)=\sum_c\Prob(B\given c)\Prob(c\given A)$.
:::

### گراف‌های تصادفی

::: {.card t="گراف اردوش–رنی" ref="5:s2 5:s3"}
در $G(n,p)$ هر یال مستقلاً با احتمال $p$ وجود دارد.

- احتمال وجود مثلث در گراف ۴ رأسی: $4p^3-6p^5+3p^6$
- کران وجود $r$-کلیک: $\Prob\le\dbinom nr p^{\binom r2}$
- با $\binom nr\le\big(\frac{ne}{r}\big)^r$: اگر $r\ge4$ و $r\ge1+\frac{2\log(ne)}{\log(1/p)}$، این احتمال حداکثر $r^{-r}$ است.
:::

## متغیر تصادفی

### تعریف‌ها و توابع توزیع

::: {.card t="متغیر تصادفی و PMF" ref="6:s1 6:s2"}
تابع $X:\Omega\to\R$ که $\{X\le x\}$ برای هر $x$ یک رویداد باشد.
$$P_X(x)=\Prob(X=x),\qquad \sum_xP_X(x)=1$$
:::

::: {.card t="تابع توزیع انباشته (CDF)" ref="7:s2"}
$$F_X(x)=\Prob(X\le x)$$

نانزولی، از راست پیوسته، $F(-\infty)=0$ و $F(\infty)=1$.
$$\Prob(a<X\le b)=F(b)-F(a),\qquad \Prob(X=x)=F(x)-F(x^-)$$
:::

::: {.card t="تابع چگالی احتمال (PDF)" ref="7:s3"}
$$f_X(x)=\frac{\dd F_X(x)}{\dd x},\qquad f\ge0,\qquad \int_{-\infty}^{\infty}f_X(x)\dd x=1$$
$$\Prob(a\le X\le b)=\int_a^bf_X(x)\dd x,\qquad \Prob(x<X\le x+\Delta)\approx f_X(x)\Delta$$
:::

::: {.card t="تساوی تقریباً حتمی و i.i.d." ref="8:s1 8:s3"}
$X=Y$ تقریباً حتمی (a.s.) یعنی $\Prob(X\ne Y)=0$.

[i.i.d.]{.en}: متغیرهای مستقل با توزیع یکسان.
:::

::: {.card t="استقلال دو متغیر تصادفی" ref="8:s2"}
$$\Prob(X\in A,\,Y\in B)=\Prob(X\in A)\,\Prob(Y\in B)\quad\forall A,B$$

معادل: $F_{XY}=F_XF_Y$ یا $f_{XY}=f_Xf_Y$.
:::

::: {.card t="متغیر مخلوط و دلتای دیراک" ref="8:s5"}
$$f_X(x)=\sum_kp_k\,\delta(x-x_k)+f_c(x)$$
$$\int g(x)\,\delta(x-a)\dd x=g(a)\qquad(\text{خاصیت غربالی})$$

هر PMF را می‌توان با دلتا به صورت PDF نوشت.
:::

### توزیع‌های گسسته

::: {.wide t="جدول توزیع‌های گسسته" ref="6:s3 9:s5-3 10:s3-1 11:s2-4"}
| توزیع | $P(X=k)$ | مقادیر | میانگین | واریانس | $M_X(t)$ |
|---|---|---|---|---|---|
| برنولی $(p)$ | $p^k(1-p)^{1-k}$ | $\{0,1\}$ | $p$ | $p(1-p)$ | $1-p+pe^t$ |
| دوجمله‌ای $(n,p)$ | $\binom nkp^k(1-p)^{n-k}$ | $0,\ldots,n$ | $np$ | $np(1-p)$ | $(1-p+pe^t)^n$ |
| هندسی $(p)$ | $(1-p)^{k-1}p$ | $1,2,\ldots$ | $\frac1p$ | $\frac{1-p}{p^2}$ | $\frac{pe^t}{1-(1-p)e^t}$ |
| پواسون $(\lambda)$ | $e^{-\lambda}\frac{\lambda^k}{k!}$ | $0,1,\ldots$ | $\lambda$ | $\lambda$ | $e^{\lambda(e^t-1)}$ |
| یکنواخت گسسته | $\frac1n$ | $1,\ldots,n$ | $\frac{n+1}2$ | $\frac{n^2-1}{12}$ | $\frac1n\sum_ke^{tk}$ |

چندجمله‌ای: $\Prob(K_1=k_1,\ldots,K_r=k_r)=\frac{n!}{k_1!\cdots k_r!}p_1^{k_1}\cdots p_r^{k_r}$ با $\E K_i=np_i$ و $\Var K_i=np_i(1-p_i)$.
:::

::: {.card t="تقریب پواسون" ref="6:s3-5"}
اگر $n\to\infty$ و $p\to0$ با $np=\lambda$:
$$\binom nkp^k(1-p)^{n-k}\to e^{-\lambda}\frac{\lambda^k}{k!}$$
:::

### توزیع‌های پیوسته

::: {.wide t="جدول توزیع‌های پیوسته" ref="7:s4 9:s5-4 10:s3-2 17:s1-1"}
| توزیع | $f_X(x)$ | تکیه‌گاه | میانگین | واریانس | $M_X(t)$ |
|---|---|---|---|---|---|
| یکنواخت $(a,b)$ | $\frac{1}{b-a}$ | $[a,b]$ | $\frac{a+b}2$ | $\frac{(b-a)^2}{12}$ | $\frac{e^{tb}-e^{ta}}{t(b-a)}$ |
| نمایی $(\lambda)$ | $\lambda e^{-\lambda x}$ | $x\ge0$ | $\frac1\lambda$ | $\frac1{\lambda^2}$ | $\frac{\lambda}{\lambda-t}$ |
| گاوسی $(\mu,\sigma^2)$ | $\frac{1}{\sqrt{2\pi}\sigma}e^{-\frac{(x-\mu)^2}{2\sigma^2}}$ | $\R$ | $\mu$ | $\sigma^2$ | $e^{\mu t+\sigma^2t^2/2}$ |
| لاپلاس $(\mu,b)$ | $\frac1{2b}e^{-\lvert x-\mu\rvert/b}$ | $\R$ | $\mu$ | $2b^2$ | $\frac{e^{\mu t}}{1-b^2t^2}$ |
| بتا $(\alpha,\beta)$ | $\frac{x^{\alpha-1}(1-x)^{\beta-1}}{B(\alpha,\beta)}$ | $[0,1]$ | $\frac{\alpha}{\alpha+\beta}$ | $\frac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}$ | — |
| ارلانگ $(k,\lambda)$ | $\frac{\lambda^kx^{k-1}e^{-\lambda x}}{(k-1)!}$ | $x\ge0$ | $\frac k\lambda$ | $\frac k{\lambda^2}$ | $\big(\frac{\lambda}{\lambda-t}\big)^k$ |
| رایلی $(\sigma)$ | $\frac{x}{\sigma^2}e^{-x^2/(2\sigma^2)}$ | $x\ge0$ | $\sigma\sqrt{\pi/2}$ | $\frac{4-\pi}{2}\sigma^2$ | — |
| کای‌دو $(k)$ | $\frac{x^{k/2-1}e^{-x/2}}{2^{k/2}\Gamma(k/2)}$ | $x\ge0$ | $k$ | $2k$ | $(1-2t)^{-k/2}$ |
| لاگ‌نرمال $(\mu,\sigma)$ | $\frac{1}{x\sigma\sqrt{2\pi}}e^{-\frac{(\ln x-\mu)^2}{2\sigma^2}}$ | $x>0$ | $e^{\mu+\sigma^2/2}$ | $(e^{\sigma^2}-1)e^{2\mu+\sigma^2}$ | — |
| کوشی $(x_0,\gamma)$ | $\frac{1}{\pi\gamma\left[1+\left(\frac{x-x_0}{\gamma}\right)^2\right]}$ | $\R$ | ندارد | ندارد | — |

MGF نمایی و ارلانگ برای $t<\lambda$، لاپلاس برای $\lvert t\rvert<1/b$ و کای‌دو برای $t<\frac12$ تعریف شده است.
:::

::: {.card t="گاوسی استاندارد" ref="7:s4-3 9:s5-4"}
$$Z=\frac{X-\mu}{\sigma}\sim\mathcal N(0,1),\qquad \Prob(a<X\le b)=\Phi\Big(\frac{b-\mu}{\sigma}\Big)-\Phi\Big(\frac{a-\mu}{\sigma}\Big)$$

$\Phi(-z)=1-\Phi(z)$. قاعده ۶۸–۹۵–۹۹٫۷: احتمال ماندن در فاصله $\sigma$، $2\sigma$ و $3\sigma$ از میانگین.
:::

### توزیع شرطی، بی‌حافظگی و مدل مخلوط

::: {.card t="توزیع شرطی" ref="9:s1"}
$$F_X(x\given B)=\frac{\Prob(X\le x,\,B)}{\Prob(B)}$$

مثلاً $f_X(x\given X\le a)=\dfrac{f_X(x)}{F_X(a)}$ برای $x\le a$ و صفر در غیر این صورت.
:::

::: {.card t="بی‌حافظگی" ref="7:s4-2 9:s2"}
$$\Prob(X>s+t\given X>s)=\Prob(X>t)$$

تنها توزیع پیوسته بی‌حافظه نمایی است (و تنها توزیع گسسته، هندسی). برای نمایی: $f_X(x\given X>a)=\lambda e^{-\lambda(x-a)}$ برای $x>a$.
:::

::: {.card t="مدل مخلوط" ref="9:s3"}
$$f_X(x)=\sum_{i=1}^np_i\,f_X(x\given\theta_i),\qquad\sum_ip_i=1$$

نمونه‌برداری: ابتدا مؤلفه $i$ را با احتمال $p_i$ و سپس نمونه را از $f(\cdot\given\theta_i)$ بگیرید. معروف‌ترین نمونه: مدل مخلوط گاوسی (GMM).
:::

### میانگین

::: {.card t="میانگین (امید ریاضی)" ref="9:s5"}
$$\E X=\sum_xx\,P_X(x),\qquad \E X=\int_{-\infty}^{\infty}x\,f_X(x)\dd x$$

به شرط همگرایی مطلق، یعنی $\E\lvert X\rvert<\infty$.
:::

::: {.card t="میانگین تابعی از متغیر" ref="10:s1"}
$$\E[g(X)]=\int g(x)f_X(x)\dd x,\qquad \E[g(X,Y)]=\iint g(x,y)f_{XY}(x,y)\dd x\dd y$$
:::

::: {.card t="خواص میانگین" ref="9:s6"}
$$\E[aX+bY+c]=a\E X+b\E Y+c\quad(\text{همیشه})$$
$$X,Y\ \text{مستقل}\ \Rightarrow\ \E[XY]=\E X\,\E Y$$
:::

::: {.card t="نامساوی ینسن" ref="9:s6"}
برای $g$ محدب:
$$g(\E X)\le\E[g(X)]$$

مثلاً $(\E X)^2\le\E X^2$ و برای $X>0$: $\E\frac1X\ge\frac{1}{\E X}$.
:::

::: {.card t="قانون اعداد بزرگ" ref="9:s7 18:s1-2"}
برای $X_i$های [i.i.d.]{.en} با میانگین $\mu$:
$$\bar X_n=\frac1n\sum_{i=1}^nX_i\ \xrightarrow{n\to\infty}\ \mu$$

صورت ضعیف (با واریانس متناهی): $\Prob(\lvert\bar X_n-\mu\rvert\ge\varepsilon)\le\dfrac{\sigma^2}{n\varepsilon^2}$.
:::

::: {.card t="توزیع بدون میانگین: کوشی" ref="9:s8"}
برای کوشی $\int\lvert x\rvert f(x)\dd x=\infty$، پس میانگین وجود ندارد. میانگین نمونه‌ای $n$ کوشی مستقل دوباره کوشی است و همگرا نمی‌شود.
:::

::: {.card t="سکه با احتمال نامعلوم (بیزی)" ref="9:s9"}
با پیشین $p\sim\mathcal U(0,1)$ و مشاهده $k$ شیر در $n$ پرتاب:
$$f(p\given\text{داده})=\frac{p^k(1-p)^{n-k}}{B(k+1,\,n-k+1)}$$

یعنی پسین $\mathrm{Beta}(k+1,n-k+1)$ با میانگین $\frac{k+1}{n+2}$.
:::

### واریانس، مد و میانه

::: {.card t="واریانس و انحراف معیار" ref="10:s2"}
$$\Var X=\E\big[(X-\E X)^2\big]=\E X^2-(\E X)^2,\qquad \sigma_X=\sqrt{\Var X}$$
$$\Var(aX+b)=a^2\Var X$$
:::

::: {.card t="واریانس جمع i.i.d." ref="10:s4"}
برای متغیرهای مستقل $\Var\big(\sum_iX_i\big)=\sum_i\Var X_i$، پس:
$$\Var\Big(\sum_{i=1}^nX_i\Big)=n\sigma^2,\qquad \Var\bar X_n=\frac{\sigma^2}{n}$$
:::

::: {.card t="مد و میانه" ref="10:s5"}
**مد:** نقطه بیشینه $f_X$ (یا $P_X$). **میانه** $m$: $\Prob(X\le m)\ge\frac12$ و $\Prob(X\ge m)\ge\frac12$.

$\E\lvert X-c\rvert$ با $c=\text{میانه}$ و $\E(X-c)^2$ با $c=\E X$ کمینه می‌شود. در چولگی به راست معمولاً $\text{مد}<\text{میانه}<\text{میانگین}$.
:::

### گشتاورها، MGF و تابع مشخصه

::: {.card t="گشتاورها، چولگی و کشیدگی" ref="11:s1"}
$$m_n=\E X^n,\qquad \mu_n=\E(X-\mu)^n$$
$$\text{چولگی}=\frac{\E(X-\mu)^3}{\sigma^3},\qquad \text{کشیدگی}=\frac{\E(X-\mu)^4}{\sigma^4}$$

کشیدگی گاوسی برابر ۳ است.
:::

::: {.card t="تابع مولد گشتاور (MGF)" ref="11:s2"}
$$M_X(t)=\E\big[e^{tX}\big],\qquad M_X^{(n)}(0)=\E X^n$$
$$M_{aX+b}(t)=e^{bt}M_X(at)$$

برای $X,Y$ مستقل: $M_{X+Y}(t)=M_X(t)\,M_Y(t)$.
:::

::: {.card t="تابع مشخصه" ref="11:s3"}
$$\Phi_X(\omega)=\E\big[e^{j\omega X}\big]=M_X(j\omega)$$

برای هر توزیعی وجود دارد و $\lvert\Phi_X(\omega)\rvert\le\Phi_X(0)=1$. همچنین $\Phi^{(n)}(0)=j^n m_n$ و برای مستقل‌ها $\Phi_{X+Y}=\Phi_X\Phi_Y$. **یکتایی:** تابع مشخصه، توزیع را به طور یکتا تعیین می‌کند.
:::

::: {.wide t="توابع مشخصه توزیع‌های معروف" ref="11:s3-2"}
| توزیع | $\Phi_X(\omega)$ |
|---|---|
| گاوسی $\mathcal N(\mu,\sigma^2)$ | $e^{j\mu\omega-\sigma^2\omega^2/2}$ |
| نمایی $(\lambda)$ | $\big(1-\frac{j\omega}{\lambda}\big)^{-1}$ |
| یکنواخت $(a,b)$ | $e^{j\omega\frac{a+b}{2}}\,\frac{\sin((b-a)\omega/2)}{(b-a)\omega/2}$ |
| برنولی $(p)$ | $pe^{j\omega}+1-p$ |
| کوشی $(x_0,\gamma)$ | $e^{jx_0\omega-\gamma\lvert\omega\rvert}$ |
:::

### توابعی از یک متغیر تصادفی

::: {.card t="حالت کلی" ref="11:s4 12:s1"}
$$F_Y(y)=\Prob(g(X)\le y)$$

حالت گسسته: $P_Y(y)=\sum_{x:\,g(x)=y}P_X(x)$. تبدیل خطی: $f_{aX+b}(y)=\dfrac{1}{\lvert a\rvert}f_X\Big(\dfrac{y-b}{a}\Big)$.
:::

::: {.card t="تبدیل یک‌به‌یک" ref="12:s2"}
$$f_Y(y)=f_X\big(g^{-1}(y)\big)\,\left|\frac{\dd g^{-1}(y)}{\dd y}\right|$$
:::

::: {.card t="تبدیل کلی" ref="12:s3 12:s5"}
اگر $x_1,x_2,\ldots$ ریشه‌های $g(x)=y$ باشند:
$$f_Y(y)=\sum_k\frac{f_X(x_k)}{\lvert g'(x_k)\rvert}$$

مثال $Y=X^2$: $f_Y(y)=\dfrac{f_X(\sqrt y)+f_X(-\sqrt y)}{2\sqrt y}$ برای $y>0$.
:::

::: {.card t="تبدیل توزیع‌ها" ref="12:s6 12:s7"}
**انتگرال احتمال:** اگر $F_X$ پیوسته باشد، $U=F_X(X)\sim\mathcal U(0,1)$.

**تبدیل معکوس:** اگر $U\sim\mathcal U(0,1)$، آنگاه $X=F^{-1}(U)$ دارای CDF برابر $F$ است. مثلاً $X=-\frac1\lambda\ln(1-U)\sim\mathrm{Exp}(\lambda)$.
:::

## چند متغیر تصادفی

### توزیع مشترک

::: {.card t="CDF مشترک" ref="13:s1"}
$$F_{XY}(x,y)=\Prob(X\le x,\,Y\le y),\qquad F_X(x)=F_{XY}(x,\infty)$$

احتمال مستطیل:
$$\begin{aligned}\Prob(x_1<X\le x_2,\,y_1<Y\le y_2)={}&F(x_2,y_2)-F(x_1,y_2)\\&-F(x_2,y_1)+F(x_1,y_1)\end{aligned}$$
:::

::: {.card t="چگالی مشترک" ref="13:s2"}
$$f_{XY}(x,y)=\frac{\partial^2F_{XY}}{\partial x\,\partial y},\qquad \Prob\big((X,Y)\in S\big)=\iint_Sf_{XY}\dd x\dd y$$
:::

::: {.card t="حاشیه‌سازی" ref="13:s3 13:s4"}
$$f_X(x)=\int_{-\infty}^{\infty}f_{XY}(x,y)\dd y,\qquad P_X(x)=\sum_yP_{XY}(x,y)$$

برای چند متغیر، روی متغیرهای ناخواسته انتگرال بگیرید.
:::

::: {.card t="استقلال" ref="13:s1 14:s2"}
$$f_{XY}(x,y)=f_X(x)f_Y(y)\iff F_{XY}=F_XF_Y$$

اگر $X,Y$ مستقل باشند، $g(X)$ و $h(Y)$ هم مستقل‌اند.
:::

### چگالی شرطی و میانگین شرطی

::: {.card t="چگالی شرطی و قانون بیز" ref="14:s3"}
$$f_{Y|X}(y\given x)=\frac{f_{XY}(x,y)}{f_X(x)},\qquad f_{XY}=f_X\,f_{Y|X}$$
$$f_{X|Y}(x\given y)=\frac{f_{Y|X}(y\given x)f_X(x)}{\int f_{Y|X}(y\given x')f_X(x')\dd x'}$$
:::

::: {.card t="میانگین شرطی" ref="14:s4"}
$$\E[Y\given X=x]=\int y\,f_{Y|X}(y\given x)\dd y$$

$\E[Y\given X]$ خودش یک متغیر تصادفی (تابعی از $X$) است.
:::

::: {.card t="میانگین کل و واریانس کل" ref="14:s4 20:s3"}
$$\E\big[\E[Y\given X]\big]=\E Y$$
$$\Var Y=\E\big[\Var(Y\given X)\big]+\Var\big(\E[Y\given X]\big)$$
:::

::: {.card t="مشترکاً گاوسی" ref="14:s5"}
با $|r|<1$:
$$f_{XY}(x,y)=\frac{1}{2\pi\sigma\sigma'\sqrt{1-r^2}}\exp\Big[\frac{-Q(x,y)}{2(1-r^2)}\Big]$$
$$Q=\frac{(x-\mu)^2}{\sigma^2}+\frac{(y-\mu')^2}{\sigma'^2}-\frac{2r(x-\mu)(y-\mu')}{\sigma\sigma'}$$
:::

::: {.card t="خواص مشترکاً گاوسی" ref="14:s5-2 15:s1"}
- حاشیه‌ها گاوسی‌اند: $X\sim\mathcal N(\mu,\sigma^2)$ و $Y\sim\mathcal N(\mu',\sigma'^2)$.
- ناهمبستگی ($r=0$) یعنی استقلال.
- $X\given Y=y\sim\mathcal N\Big(\mu+r\frac{\sigma}{\sigma'}(y-\mu'),\ (1-r^2)\sigma^2\Big)$
- هر ترکیب خطی $aX+bY$ گاوسی است. منحنی‌های تراز بیضی‌اند و $|r|=1$ یعنی $Y$ تابع خطی $X$ است.
:::

### کوواریانس و همبستگی

::: {.card t="گشتاور مشترک و کوواریانس" ref="15:s3 15:s4"}
$$m_{kr}=\E[X^kY^r]$$
$$\Cov(X,Y)=\E\big[(X-\mu_X)(Y-\mu_Y)\big]=\E[XY]-\E X\,\E Y$$
$$\Cov(aX+b,\,cY+d)=ac\,\Cov(X,Y)$$
:::

::: {.card t="ضریب همبستگی" ref="15:s4 15:s5"}
$$\rho_{XY}=\frac{\Cov(X,Y)}{\sigma_X\sigma_Y},\qquad \lvert\rho\rvert\le1$$

از نامساوی کوشی–شوارتز $(\E XY)^2\le\E X^2\,\E Y^2$. همچنین $|\rho|=1$ اگر و تنها اگر $Y=aX+b$ (a.s.).
:::

::: {.card t="واریانس جمع" ref="15:s4"}
$$\Var(X\pm Y)=\Var X+\Var Y\pm2\Cov(X,Y)$$
$$\Var\Big(\sum_ia_iX_i\Big)=\sum_i\sum_ja_ia_j\Cov(X_i,X_j)$$
:::

::: {.card t="ناهمبستگی و استقلال" ref="15:s5-1"}
$\text{مستقل}\Rightarrow\text{ناهمبسته}\ (\Cov=0)$، ولی عکس آن درست نیست. مثال: $X\sim\mathcal U(-1,1)$ و $Y=X^2$ ناهمبسته‌اند ولی وابسته. برای مشترکاً گاوسی‌ها این دو معادل‌اند. **متعامد** یعنی $\E[XY]=0$.
:::

::: {.card t="توزیع‌های مشترک تکین" ref="15:s2"}
اگر جرم احتمال روی نقطه‌ها یا روی یک خط (مثلاً $Y=aX+b$) متمرکز باشد، چگالی مشترک معمولی وجود ندارد و باید با دلتا یا با CDF کار کرد.
:::

### تابعی از دو متغیر و جمع

::: {.card t="حالت کلی $Z=g(X,Y)$" ref="16:s2"}
$$F_Z(z)=\Prob\big(g(X,Y)\le z\big)=\iint_{g(x,y)\le z}f_{XY}(x,y)\dd x\dd y$$
:::

::: {.card t="جمع: کانولوشن" ref="16:s3 16:s4"}
گسسته: $\Prob(X+Y=z)=\sum_k\Prob(X=k,\,Y=z-k)$. پیوسته:
$$f_{X+Y}(z)=\int f_{XY}(x,z-x)\dd x\ \overset{\text{مستقل}}{=}\ \int f_X(x)f_Y(z-x)\dd x$$
:::

::: {.card t="جمع توزیع‌های معروف (مستقل)" ref="16:s5 16:s6 11:s2-3"}
- $\mathcal N(\mu_1,\sigma_1^2)+\mathcal N(\mu_2,\sigma_2^2)=\mathcal N(\mu_1+\mu_2,\sigma_1^2+\sigma_2^2)$
- $\mathrm{Pois}(\lambda_1)+\mathrm{Pois}(\lambda_2)=\mathrm{Pois}(\lambda_1+\lambda_2)$
- $\mathrm{Bin}(n,p)+\mathrm{Bin}(m,p)=\mathrm{Bin}(n+m,p)$
- جمع $k$ نمایی $(\lambda)$ برابر ارلانگ $(k,\lambda)$ است.
- $\mathcal U(0,1)+\mathcal U(0,1)$ چگالی مثلثی روی $[0,2]$ دارد. مجموع دو تاس: $\frac{6-|z-7|}{36}$.
:::

### توابع معروف، آماره‌های ترتیبی و قضیه حد مرکزی

::: {.card t="کای‌دو، رایلی و نسبت" ref="17:s1"}
اگر $X_i$ها [i.i.d.]{.en} و $\mathcal N(0,1)$ باشند: $\sum_{i=1}^kX_i^2\sim\chi^2(k)$.

اگر $X,Y$ [i.i.d.]{.en} و $\mathcal N(0,\sigma^2)$ باشند:
$$\sqrt{X^2+Y^2}\sim\text{رایلی}(\sigma),\qquad \frac XY\sim\text{کوشی}(0,1)$$
:::

::: {.card t="کمینه و بیشینه" ref="17:s2"}
برای $n$ نمونه [i.i.d.]{.en} با $F,f$:
$$F_{\max}=F^n,\qquad f_{\max}=nf\,F^{n-1}$$
$$F_{\min}=1-(1-F)^n,\qquad f_{\min}=nf\,(1-F)^{n-1}$$

آماره ترتیبی $k$ام: $f_{(k)}=\frac{n!}{(k-1)!(n-k)!}F^{k-1}(1-F)^{n-k}f$.
:::

::: {.card t="قضیه حد مرکزی" ref="17:s3"}
برای $X_i$های [i.i.d.]{.en} با میانگین $\mu$ و واریانس متناهی $\sigma^2$:
$$Z_n=\frac{\sum_{i=1}^n(X_i-\mu)}{\sigma\sqrt n},\qquad \lim_{n\to\infty}\Prob(Z_n\le z)=\Phi(z)$$

در عمل $\sum X_i\approx\mathcal N(n\mu,n\sigma^2)$ و $\bar X_n\approx\mathcal N(\mu,\sigma^2/n)$.
:::

## آمار و تخمین

### نامساوی‌های احتمالاتی

::: {.card t="نامساوی مارکوف" ref="18:s1-1"}
برای $X\ge0$ و $a>0$:
$$\Prob(X\ge a)\le\frac{\E X}{a}$$
:::

::: {.card t="نامساوی چبیشف" ref="18:s1-2"}
$$\Prob\big(\lvert X-\mu\rvert\ge k\sigma\big)\le\frac1{k^2},\qquad \Prob\big(\lvert X-\mu\rvert\ge\varepsilon\big)\le\frac{\sigma^2}{\varepsilon^2}$$

برای هر توزیعی با واریانس متناهی برقرار است.
:::

### مفاهیم آماری

::: {.card t="آمار در مقابل احتمال" ref="18:s2 19:s1"}
**احتمال (قیاسی):** از مدل $f_X(x;\theta)$ به داده‌ها. **آمار (استقرایی):** از داده‌های $X_1,\ldots,X_n$ به مدل. سه سرفصل اصلی: تخمین، آزمون فرض و پیش‌بینی.
:::

::: {.card t="CDF تجربی" ref="19:s2-1"}
$$\hat F_n(x)=\frac1n\sum_{i=1}^n\ind(X_i\le x)$$
$$\E\hat F_n(x)=F(x),\qquad \Var\hat F_n(x)=\frac{F(x)\big(1-F(x)\big)}{n}$$
:::

::: {.card t="هیستوگرام" ref="19:s2-2"}
$$\hat f(x)=\frac{\text{تعداد نمونه‌ها در خانه شامل }x}{n\,h}$$

$h$ عرض هر خانه است.
:::

::: {.card t="میانگین و واریانس نمونه‌ای" ref="19:s2-3 22:s4-2"}
$$\bar X_n=\frac1n\sum_iX_i,\qquad S^2=\frac{1}{n-1}\sum_{i=1}^n(X_i-\bar X_n)^2,\qquad \E S^2=\sigma^2$$

ضریب $\frac1{n-1}$ گرایش را حذف می‌کند، چون $\sum(X_i-\mu)^2=\sum(X_i-\bar X)^2+n(\bar X-\mu)^2$.
:::

::: {.card t="بازه اطمینان برای میانگین" ref="19:s3-2"}
$$\Prob\Big(\bar X_n-z_{\delta/2}\frac{\sigma}{\sqrt n}<\mu<\bar X_n+z_{\delta/2}\frac{\sigma}{\sqrt n}\Big)=1-\delta$$

$z_{0.025}=1.96$ (۹۵٪) و $z_{0.005}=2.576$ (۹۹٪).
:::

::: {.card t="تخمین بیزی" ref="19:s3-3"}
$$f(\theta\given x_{1:n})\propto f(x_{1:n}\given\theta)\,f(\theta)$$

تخمین نقطه‌ای از پسین: نقطه بیشینه (MAP) یا میانگین پسین.
:::

::: {.card t="آزمون فرض" ref="19:s4"}
فرض صفر $H_0$ و فرض مقابل $H_1$، آماره آزمون $T$ و ناحیه رد $R$.

- خطای نوع اول (رد $H_0$ درست): $\alpha$، سطح معناداری
- خطای نوع دوم (نپذیرفتن $H_1$ درست): $\beta$
- توان آزمون: $1-\beta$
:::

### تخمین میانگین مربع (MS)

::: {.card t="تخمین با یک ثابت" ref="20:s1-2"}
$$\min_c\E(X-c)^2:\quad c^*=\E X,\qquad \text{خطا}=\Var X$$
:::

::: {.card t="خطی همگن $\hat Y=aX$" ref="20:s1-3"}
$$a^*=\frac{\E(XY)}{\E(X^2)}$$
:::

::: {.card t="خطی غیرهمگن $\hat Y=aX+b$" ref="20:s1-4"}
$$a^*=\frac{\Cov(X,Y)}{\sigma_X^2},\qquad b^*=\mu_Y-a^*\mu_X$$
$$\hat Y=\mu_Y+\rho\frac{\sigma_Y}{\sigma_X}(X-\mu_X),\qquad \mathrm{MSE}_{\min}=\sigma_Y^2(1-\rho^2)$$

اصل تعامد: خطای $e=Y-\hat Y$ با $\E e=0$ و $\E[eX]=0$.
:::

::: {.card t="تخمین‌گر غیرخطی بهینه" ref="20:s1-5 20:s1-6"}
$$\varphi^*(X)=\E[Y\given X]$$

ترتیب خطاها: $\text{غیرخطی}\le\text{خطی غیرهمگن}\le\text{خطی همگن}$. برای مشترکاً گاوسی‌ها $\E[Y\given X]$ خطی است، پس بهترین تخمین‌گر خطی همان بهترین تخمین‌گر کلی است.
:::

::: {.card t="حالت چندمتغیره" ref="20:s1-7"}
$$\hat Y=\sum_ia_iX_i+b,\qquad \mathbf a=\Sigma^{-1}\mathbf c,\qquad b=\E Y-\sum_ia_i\E X_i$$

$\Sigma_{ij}=\Cov(X_i,X_j)$ و $c_i=\Cov(X_i,Y)$.
:::

### تخمین نقطه‌ای

::: {.card t="گرایش، واریانس و سازگاری" ref="20:s2-2"}
$$\mathrm{Bias}(\hat\theta)=\E\{\theta-\hat\theta\},\qquad \Var(\hat\theta)=\E\big[(\hat\theta-\E\hat\theta)^2\big]$$

**سازگار:** $\hat\theta\to\theta$ وقتی $n\to\infty$. شرط کافی: گرایش و واریانس هر دو به صفر میل کنند. این سه ویژگی مستقل از هم‌اند.
:::

::: {.card t="تجزیه گرایش–واریانس" ref="20:s2-3"}
$$\mathrm{MSE}(\hat\theta)=\E(\hat\theta-\theta)^2=\mathrm{Bias}^2+\Var(\hat\theta)$$

گاهی کمی گرایش، واریانس را آن‌قدر کم می‌کند که MSE کمتر شود.
:::

::: {.card t="مقایسه تخمین‌گرهای واریانس (گاوسی)" ref="20:s2-3"}
برای $c\sum(X_i-\bar X)^2$:

- $c=\frac1{n-1}$ (بی‌گرایش): $\mathrm{MSE}=\frac{2\sigma^4}{n-1}$
- $c=\frac1n$ (MLE): $\mathrm{MSE}=\frac{(2n-1)\sigma^4}{n^2}$
- $c=\frac1{n+1}$ (کمینه MSE): $\mathrm{MSE}=\frac{2\sigma^4}{n+1}$
:::

::: {.card t="انواع تخمین‌گرها" ref="20:s2-4"}
- MVUE: بی‌گرایش با کمینه واریانس
- MMSE: کمینه میانگین مربعات خطا
- MLE: بیشینه درست‌نمایی
- MoME: روش گشتاورها
:::

### تخمین‌گر بیشینه درست‌نمایی (MLE)

::: {.card t="تعریف MLE" ref="21:s3"}
$$\hat\theta_\ML=\argmax_{\theta}\prod_{i=1}^nf_X(X_i;\theta)=\argmax_\theta\ LL(\theta)$$
$$LL(\theta)=\sum_{i=1}^n\log f_X(X_i;\theta)$$

در حالت گسسته $f_X$ با $P_X$ جایگزین می‌شود.
:::

::: {.card t="روش محاسبه" ref="21:s3-3 22:s1 22:s2"}
1. حل معادله $\frac{\partial}{\partial\theta}LL=0$ و بررسی بیشینه بودن (مشتق دوم یا مرزها)
2. اگر تکیه‌گاه به $\theta$ وابسته باشد، $L(\theta)$ را مستقیم بررسی کنید؛ جواب معمولاً روی لبه است.
3. پارامتر گسسته: جست‌وجو در فضای گسسته (ممکن است NP-سخت باشد).
:::

::: {.card t="خواص MLE" ref="21:s4 21:s6"}
تحت شرایط نظم سازگار است، ولی لزوماً بی‌گرایش نیست.

**ناوردایی:** $\widehat{g(\theta)}_\ML=g(\hat\theta_\ML)$.
:::

::: {.card t="کران کرامر–رائو" ref="21:s5-1"}
برای هر تخمین‌گر بی‌گرایش:
$$\Var(\hat\theta)\ge\frac{1}{nI(\theta)},\qquad I(\theta)=\E\Big[\Big(\frac{\partial\log f}{\partial\theta}\Big)^2\Big]=-\E\Big[\frac{\partial^2\log f}{\partial\theta^2}\Big]$$

مجانباً $\sqrt n(\hat\theta_\ML-\theta)\to\mathcal N\big(0,\frac{1}{I(\theta)}\big)$.
:::

::: {.wide t="جدول MLE مدل‌های مهم" ref="21:s5 21:s7 22:s1 22:s3 22:s4"}
| مدل | پارامتر | $\hat\theta_\ML$ | $\E\hat\theta_\ML$ | تخمین‌گر بی‌گرایش |
|---|---|---|---|---|
| برنولی | $p$ | $\bar X_n$ | $p$ | خودش |
| پواسون | $\lambda$ | $\bar X_n$ | $\lambda$ | خودش |
| گاوسی، $\sigma$ معلوم | $\mu$ | $\bar X_n$ | $\mu$ | خودش (واریانس $\sigma^2/n$) |
| گاوسی، $\mu$ معلوم | $\sigma^2$ | $\frac1n\sum(X_i-\mu)^2$ | $\sigma^2$ | خودش |
| گاوسی، هر دو نامعلوم | $(\mu,\sigma^2)$ | $\big(\bar X_n,\ \frac1n\sum(X_i-\bar X_n)^2\big)$ | $\big(\mu,\ \frac{n-1}n\sigma^2\big)$ | $S^2=\frac{1}{n-1}\sum(X_i-\bar X_n)^2$ |
| نمایی | $\lambda$ | $\frac1{\bar X_n}$ | $\frac{n\lambda}{n-1}$ | $\frac{n-1}{\sum X_i}$ |
| هندسی | $p$ | $\frac1{\bar X_n}$ | — | — |
| رایلی | $\sigma^2$ | $\frac{1}{2n}\sum X_i^2$ | $\sigma^2$ | خودش |
| یکنواخت $(0,\theta)$ | $\theta$ | $\max_iX_i$ | $\frac{n}{n+1}\theta$ | $\frac{n+1}{n}\max_iX_i$ |
| یکنواخت $(a,b)$ | $(a,b)$ | $(\min_iX_i,\ \max_iX_i)$ | — | — |
| نمایی انتقال‌یافته | $\theta$ | $\min_iX_i$ | $\theta+\frac1n$ | $\min_iX_i-\frac1n$ |
| لاپلاس (مکان) | $\theta$ | میانه نمونه‌ای | — | — |
| یک کارت از $1..n$ | $n$ | $X$ | $\frac{n+1}2$ | $2X-1$ |
| $k$ کارت (تانک آلمانی) | $N$ | $M=\max$ | $\frac{k(N+1)}{k+1}$ | $\frac{k+1}{k}M-1$ |

کانال دودویی متقارن با $\varepsilon<\frac12$: MLE رشته ارسالی، نزدیک‌ترین کلمه کد (کمترین فاصله همینگ) به رشته دریافتی است.
:::

## پیوست: روابط کمکی

### سری‌ها، انتگرال‌ها و جدول گاوسی

::: {.card t="سری‌ها" ref=""}
$$\sum_{k=0}^\infty x^k=\frac1{1-x},\qquad \sum_{k=1}^\infty kx^{k-1}=\frac1{(1-x)^2}\qquad(|x|<1)$$
$$\sum_{k=1}^nk=\frac{n(n+1)}2,\qquad \sum_{k=1}^nk^2=\frac{n(n+1)(2n+1)}6$$
$$e^x=\sum_{k=0}^\infty\frac{x^k}{k!},\qquad \Big(1+\frac xn\Big)^n\to e^x$$
:::

::: {.card t="انتگرال‌ها و توابع خاص" ref=""}
$$\int_{-\infty}^{\infty}e^{-x^2/2}\dd x=\sqrt{2\pi},\qquad \int_0^\infty x^ne^{-\lambda x}\dd x=\frac{n!}{\lambda^{n+1}}$$
$$\Gamma(a)=\int_0^\infty x^{a-1}e^{-x}\dd x,\quad \Gamma(n)=(n-1)!,\quad \Gamma\big(\tfrac12\big)=\sqrt\pi$$
$$B(a,b)=\int_0^1x^{a-1}(1-x)^{b-1}\dd x=\frac{\Gamma(a)\Gamma(b)}{\Gamma(a+b)}$$
:::

::: {.card t="تقریب‌ها و کران‌ها" ref="3:s6-1 5:s3"}
$$n!\approx\sqrt{2\pi n}\Big(\frac ne\Big)^n,\qquad \binom nr\le\Big(\frac{ne}{r}\Big)^r,\qquad 1-x\le e^{-x}$$
:::

::: {.wide t="مقادیر $\Phi(z)$ گاوسی استاندارد" ref="7:s4-3 19:s3-2"}
| $z$ | $0.5$ | $1$ | $1.28$ | $1.5$ | $1.645$ | $1.96$ | $2$ | $2.326$ | $2.576$ | $3$ |
|---|---|---|---|---|---|---|---|---|---|---|
| $\Phi(z)$ | $0.6915$ | $0.8413$ | $0.8997$ | $0.9332$ | $0.9500$ | $0.9750$ | $0.9772$ | $0.9900$ | $0.9950$ | $0.9987$ |

$\Prob(\lvert Z\rvert<1)=0.6827$، $\Prob(\lvert Z\rvert<2)=0.9545$ و $\Prob(\lvert Z\rvert<3)=0.9973$.
:::

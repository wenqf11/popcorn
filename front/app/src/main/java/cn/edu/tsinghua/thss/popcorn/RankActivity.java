package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Context;
import android.graphics.Color;
import android.os.Bundle;
import android.os.SystemClock;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.beardedhen.androidbootstrap.FontAwesomeText;
import com.lidroid.xutils.HttpUtils;
import com.lidroid.xutils.ViewUtils;
import com.lidroid.xutils.exception.HttpException;
import com.lidroid.xutils.http.RequestParams;
import com.lidroid.xutils.http.ResponseInfo;
import com.lidroid.xutils.http.callback.RequestCallBack;
import com.lidroid.xutils.http.client.HttpRequest;
import com.lidroid.xutils.view.annotation.ViewInject;
import com.lidroid.xutils.view.annotation.event.OnClick;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import cn.edu.tsinghua.thss.popcorn.config.Config;
import cn.edu.tsinghua.thss.popcorn.utils.NoRepeatToast;


public class RankActivity extends Activity {

    private List<Map<String, Object>> mData = null;
    private ProgressDialog progressDialog;
    private JSONArray RankList = null;
    private RankListAdapter adapter;

    @ViewInject(R.id.rank_datepicker)
    private DatePicker datePicker;

    @ViewInject(R.id.rank_submit_date)
    private Button submitDate;

    @ViewInject(R.id.rank_listview)
    private ListView lv ;

    @OnClick(R.id.rank_submit_date)
    private void submitDataClick(View v){
        updateRanListData();
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_rank);

        progressDialog = new ProgressDialog(RankActivity.this, R.style.buffer_dialog);
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.setMessage("数据加载中...");
        progressDialog.setIndeterminate(false);
        progressDialog.setCancelable(false);

        ViewUtils.inject(this);

        datePicker.setMaxDate(new Date().getTime());
        if (datePicker != null) {
            ((ViewGroup)((ViewGroup) datePicker.getChildAt(0)).getChildAt(0)).getChildAt(2).setVisibility(View.GONE);
        }

        adapter = new RankListAdapter (this);
        lv.setAdapter(adapter);
        updateRanListData();

    }

    public void updateRanListData(){
        final int pickedMonth = datePicker.getMonth()+1;
        final int pickedYear = datePicker.getYear();

        RequestParams params = new RequestParams();
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);
        params.addQueryStringParameter("year", String.valueOf(pickedYear));
        params.addQueryStringParameter("month", String.valueOf(pickedMonth));

        progressDialog.show();
//        SystemClock.sleep(3000);

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.GET,
                Config.SCORE_RANK_URL,
                params,
                new RequestCallBack<String>() {

                    @Override
                    public void onStart() {
                    }

                    @Override
                    public void onLoading(long total, long current, boolean isUploading) {
                    }

                    @Override
                    public void onSuccess(ResponseInfo<String> responseInfo) {
                        try{
                            JSONObject jsonObject = new JSONObject(responseInfo.result);
                            String status = jsonObject.getString("status");


                            if(status.equals("ok")) {
                                RankList = jsonObject.getJSONArray("data");
                            }

                        }catch (JSONException e){
                            e.printStackTrace();
                        }

                        mData = getData();
                        adapter.notifyDataSetChanged();

                        progressDialog.hide();
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        //Toast.makeText(getApplicationContext(), "网络连接异常，请检查网络连接！", Toast.LENGTH_SHORT).show();
                        NoRepeatToast.showToast(getApplicationContext(), "网络连接异常，请检查网络连接！", Toast.LENGTH_SHORT);
                        progressDialog.hide();
                    }
                });
    }

    private List<Map<String, Object>> getData() {
        List<Map<String ,Object>> list = new ArrayList<Map<String,Object>>();

        if (RankList != null) {
            for (int i = 0; i < RankList.length(); i++) {
                Map<String, Object> map = new HashMap<String, Object>();
                try {
                    JSONObject tempObject = RankList.getJSONObject(i);
                    map.put("username", tempObject.getString("username"));
                    map.put("name", tempObject.getString("name"));
                    map.put("score", tempObject.getString("score"));
                    list.add(map);
                } catch (Exception e) {
                }
            }
        }

        return list;
    }

    class ViewHolder {
        public TextView name;
        public TextView rank;
        public TextView score;
        public LinearLayout linearLayoutBg;
    }

    public class RankListAdapter extends BaseAdapter {
        private LayoutInflater mInflater = null;

        public RankListAdapter(Context context) {
            super();
            mInflater = (LayoutInflater) context
                    .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        }

        @Override
        public int getCount() {
            if (mData == null){
                return 0;
            }else{
                return mData.size();
            }
        }

        @Override
        public Object getItem(int position) {
            // TODO Auto-generated method stub
            return null;
        }

        @Override
        public long getItemId(int position) {
            // TODO Auto-generated method stub
            return position;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {

            ViewHolder holder = null;
            if (convertView == null) {
                holder = new ViewHolder();
                convertView = mInflater.inflate(R.layout.listview_rank, null);

                holder.name = (TextView) convertView.findViewById(R.id.listview_rank_name);
                holder.rank = (TextView) convertView.findViewById(R.id.listview_rank_rank);
                holder.score = (TextView) convertView.findViewById(R.id.listview_rank_score);
                holder.linearLayoutBg = (LinearLayout) convertView.findViewById(R.id.listview_rank_ll);
                convertView.setTag(holder);
            } else {
                holder = (ViewHolder) convertView.getTag();
            }

            holder.name.setText((String) mData.get(position).get("name"));
            holder.score.setText((String) mData.get(position).get("score"));
            holder.rank.setText(String.valueOf(position + 1));
            if(mData.get(position).get("username").equals(Config.DEBUG_USERNAME)) {
                holder.linearLayoutBg.setBackgroundColor(Color.parseColor("#E1FFFF"));
            }else{
                holder.linearLayoutBg.setBackgroundColor(Color.WHITE);
            }
            return convertView;
        }
    }

    @Override
    protected  void onDestroy(){
        progressDialog.dismiss();
        super.onDestroy();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.rank, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.close_btn) {
            RankActivity.this.finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
